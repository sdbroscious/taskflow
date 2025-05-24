import pytest
from datetime import datetime, timedelta, timezone
from app import db
from app.models import Task, Project
from tests.factories import TaskFactory, ProjectFactory

def test_new_task(db_session):
    """Test creating a new task."""
    # Create a test project
    project = ProjectFactory()
    db_session.add(project)
    db_session.commit()
    
    # Create a task
    task = Task(
        title='Test Task',
        description='Test Description',
        due_date=datetime.now(timezone.utc) + timedelta(days=1),
        priority=2,
        project_id=project.id
    )
    db_session.add(task)
    db_session.commit()
    
    assert task.id is not None
    assert task.title == 'Test Task'
    assert task.completed is False
    assert task.priority == 2
    assert task.project_id == project.id

def test_task_relationships(db_session):
    """Test task relationships."""
    # Create a project with tasks
    project = ProjectFactory()
    task1 = TaskFactory(project=project)
    task2 = TaskFactory(project=project)
    
    db_session.add_all([project, task1, task2])
    db_session.commit()
    
    # Test relationship from task to project
    assert task1.project == project
    assert task2.project == project
    
    # Test relationship from project to tasks
    assert task1 in project.tasks
    assert task2 in project.tasks
    assert len(project.tasks.all()) == 2

def test_task_completion(db_session):
    """Test task completion functionality."""
    task = TaskFactory(completed=False)
    db_session.add(task)
    db_session.commit()
    
    # Mark as completed
    task.completed = True
    task.completed_at = datetime.now(timezone.utc)
    db_session.commit()
    
    assert task.completed is True
    assert task.completed_at is not None

def test_project_creation(db_session):
    """Test project creation and properties."""
    project = Project(
        name='Test Project',
        color='#FF0000'
    )
    db_session.add(project)
    db_session.commit()
    
    assert project.id is not None
    assert project.name == 'Test Project'
    assert project.color == '#FF0000'
    assert project.created_at is not None

def test_project_tasks_relationship(db_session):
    """Test project's tasks relationship."""
    project = ProjectFactory()
    task1 = TaskFactory(project=project)
    task2 = TaskFactory(project=project)
    
    db_session.add_all([project, task1, task2])
    db_session.commit()
    
    # Test tasks are associated with the project
    assert project.tasks.count() == 2
    assert task1 in project.tasks
    assert task2 in project.tasks

@pytest.mark.parametrize('priority,expected', [
    (1, 'High'),
    (2, 'Medium'),
    (3, 'Low'),
    (4, 'No Priority'),
    (5, 'Unknown')
])
def test_task_priority_label(db_session, priority, expected):
    """Test task priority label generation."""
    task = TaskFactory(priority=priority)
    db_session.add(task)
    db_session.commit()
    assert task.priority_label == expected