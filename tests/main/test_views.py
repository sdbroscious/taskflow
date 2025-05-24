import pytest
from flask import url_for, get_flashed_messages, session
from app import create_app, db
from app.models import Task, Project
from tests.factories import TaskFactory, ProjectFactory

# Test configuration
TEST_CONFIG = {
    'TESTING': True,
    'WTF_CSRF_ENABLED': False,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SECRET_KEY': 'test-secret-key',
    'PRESERVE_CONTEXT_ON_EXCEPTION': False
}

def test_index_route(client):
    """Test the index route returns a 200 status code."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'TaskFlow' in response.data

def test_add_task_route_get(client):
    """Test the add task form is displayed correctly."""
    response = client.get(url_for('main.add_task'))
    assert response.status_code == 200
    assert b'Add New Task' in response.data

def test_add_task_route_post(app, client, db_session):
    """Test adding a new task."""
    # Create a test project
    project = ProjectFactory()
    db_session.add(project)
    db_session.commit()
    
    # Submit the form
    response = client.post(url_for('main.add_task'), data={
        'title': 'Test Task',
        'description': 'Test Description',
        'due_date': '2023-12-31',
        'priority': '2',
        'project_id': str(project.id)  # Ensure project_id is string for form data
    }, follow_redirects=True)
    
    # Check if task was added to the database
    task = Task.query.filter_by(title='Test Task').first()
    assert task is not None, "Task was not added to the database"
    assert task.description == 'Test Description', "Task description does not match"
    assert task.priority == 2, "Task priority does not match"
    
    # Check for success message in the response
    assert b'Task added successfully' in response.data, "Success message not found in response"
    
    # Check redirect to index
    assert response.status_code == 200
    assert b'Test Task' in response.data

def test_edit_task_route_get(client, db_session):
    """Test the edit task form is displayed with correct data."""
    # Create a test task
    task = TaskFactory(title='Original Task')
    db_session.add(task)
    db_session.commit()
    
    response = client.get(url_for('main.edit_task', task_id=task.id))
    assert response.status_code == 200
    assert b'Edit Task' in response.data
    assert b'Original Task' in response.data

def test_edit_task_route_post(app, client, db_session):
    """Test editing an existing task."""
    # Create a test task
    project = ProjectFactory()
    task = TaskFactory(title='Original Task', project=project)
    db_session.add_all([project, task])
    db_session.commit()
    
    # Submit the form
    response = client.post(
        url_for('main.edit_task', task_id=task.id),
        data={
            'title': 'Updated Task',
            'description': 'Updated Description',
            'due_date': '2023-12-31',
            'priority': '1',
            'project_id': str(project.id)
        },
        follow_redirects=True
    )
    
    # Check if task was updated in the database
    updated_task = Task.query.get(task.id)
    assert updated_task is not None, "Task not found in database"
    assert updated_task.title == 'Updated Task', "Task title was not updated"
    assert updated_task.description == 'Updated Description', "Task description was not updated"
    assert updated_task.priority == 1, "Task priority was not updated"
    
    # Check for success message in the response
    assert b'Task updated successfully' in response.data, "Success message not found in response"
    
    # Check redirect to index
    assert response.status_code == 200
    assert b'Updated Task' in response.data

def test_complete_task_route(app, client, db_session):
    """Test marking a task as completed."""
    with app.app_context():
        # Create a test task
        task = TaskFactory(completed=False)
        db_session.add(task)
        db_session.commit()
        
        # Mark task as completed
        response = client.post(
            url_for('main.complete_task', task_id=task.id),
            headers={'X-Requested-With': 'XMLHttpRequest'}
        )
        
        # Check response
        assert response.status_code == 200
        assert response.json == {'message': 'Task completed'}
        
        # Check if task was marked as completed in the database
        updated_task = db_session.get(Task, task.id)
        assert updated_task.completed is True
        assert updated_task.completed_at is not None
        
        # For AJAX requests, flash messages might not be in the session
        # So we'll just check the JSON response for success

def test_delete_task_route(app, client, db_session):
    """Test deleting a task."""
    # Create a test task
    task = TaskFactory()
    db_session.add(task)
    db_session.commit()
    task_id = task.id
    
    # Delete the task
    response = client.post(
        url_for('main.delete_task', task_id=task_id),
        follow_redirects=True
    )
    
    # Check if task was deleted from the database
    deleted_task = Task.query.get(task_id)
    assert deleted_task is None, "Task was not deleted from the database"
    
    # Check for success message in the response
    assert b'Task deleted successfully' in response.data, "Success message not found in response"
    
    # Check redirect to index
    assert response.status_code == 200

def test_task_list_display(app, client, db_session):
    """Test that tasks are displayed in the correct order."""
    # Create a project first
    project = ProjectFactory()
    
    # Create test tasks with different priorities
    task1 = TaskFactory(priority=1, title='High Priority', project=project)
    task2 = TaskFactory(priority=3, title='Low Priority', project=project)
    task3 = TaskFactory(priority=2, title='Medium Priority', project=project)
    
    db_session.add_all([project, task1, task2, task3])
    db_session.commit()
    
    # Get the index page
    response = client.get(url_for('main.index'))
    
    # Check if tasks are in the correct order in the response
    content = response.data.decode('utf-8')
    task1_pos = content.find('High Priority')
    task2_pos = content.find('Medium Priority')
    task3_pos = content.find('Low Priority')
    
    assert task1_pos != -1, "High priority task not found in response"
    assert task2_pos != -1, "Medium priority task not found in response"
    assert task3_pos != -1, "Low priority task not found in response"
    assert task1_pos < task2_pos < task3_pos, "Tasks not in correct priority order"  # Higher priority first