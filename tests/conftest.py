import os
import pytest
from datetime import datetime, timedelta, timezone

from app import create_app, db
from app.models import Task, Project

# Disable CSRF protection in testing
os.environ['WTF_CSRF_ENABLED'] = 'False'

# Test configuration
TEST_CONFIG = {
    'TESTING': True,
    'WTF_CSRF_ENABLED': False,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_ENGINE_OPTIONS': {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
    },
    'SECRET_KEY': 'test-secret-key',
    'PRESERVE_CONTEXT_ON_EXCEPTION': False
}

@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for testing."""
    # Create a new test app with test config
    app = create_app(TEST_CONFIG)
    
    # Push an application context
    ctx = app.app_context()
    ctx.push()
    
    # Create the database
    db.create_all()
    
    yield app
    
    # Clean up
    db.session.remove()
    db.drop_all()
    if hasattr(db.engine, 'dispose'):
        db.engine.dispose()
    
    # Pop the context
    ctx.pop()

@pytest.fixture
def client(app):
    """A test client for the app."""
    with app.test_client() as client:
        with client.session_transaction() as session:
            session.clear()
        yield client

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture(autouse=True)
def _setup_db(app):
    """Set up the database for each test."""
    # Ensure we're in the app context
    with app.app_context():
        # Create all tables if they don't exist
        db.create_all()
        
        # Start a new transaction
        connection = db.engine.connect()
        transaction = connection.begin()
        
        # Bind the session to the connection
        db.session = db.create_scoped_session({
            'bind': connection,
            'binds': {}
        })
        
        # Set up factory_boy sessions
        from tests.factories import TaskFactory, ProjectFactory
        TaskFactory._meta.sqlalchemy_session = db.session
        TaskFactory._meta.sqlalchemy_session_persistence = 'commit'
        ProjectFactory._meta.sqlalchemy_session = db.session
        ProjectFactory._meta.sqlalchemy_session_persistence = 'commit'
        
        yield
        
        # Clean up
        db.session.remove()
        transaction.rollback()
        connection.close()
        
        # Recreate the session for the next test
        db.session = db.create_scoped_session()

@pytest.fixture
def db_session(app):
    """Creates a new database session for a test."""
    # We don't need to create a new session here as it's already handled by _setup_db
    yield db.session
    
    # Rollback any uncommitted changes
    db.session.rollback()

@pytest.fixture
def new_project(db_session):
    """Create a new project for testing."""
    project = Project(name='Test Project', color='#00FF00')
    db_session.add(project)
    db_session.commit()
    # Refresh to ensure we have the latest data
    db_session.refresh(project)
    return project

@pytest.fixture
def new_task(db_session, new_project):
    """Create a new task for testing."""
    task = Task(
        title='Test Task',
        description='Test Description',
        project_id=new_project.id,
        due_date=datetime.now(timezone.utc) + timedelta(days=1),
        priority=2
    )
    db_session.add(task)
    db_session.commit()
    return task

@pytest.fixture
def authed_client(app, client, db_session):
    """Create an authenticated client."""
    with app.app_context():
        with client.session_transaction() as session:
            session['_user_id'] = 'test_user'
            session['_fresh'] = True
        yield client