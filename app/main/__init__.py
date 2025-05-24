from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from .. import db
from ..models import Task, Project
from .forms import TaskForm
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    tasks = Task.query.filter_by(completed=False).order_by(Task.priority.asc(), Task.due_date.asc()).all()
    return render_template('index.html', title='Home', tasks=tasks)

@main.route('/add_task', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()
    
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            priority=form.priority.data,
            project_id=form.project_id.data if hasattr(form, 'project_id') else None
        )
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('add_task.html', title='Add Task', form=form)

@main.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.due_date = form.due_date.data
        task.priority = form.priority.data
        if hasattr(form, 'project_id'):
            task.project_id = form.project_id.data
        db.session.commit()
        flash('Task updated successfully', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('edit_task.html', title='Edit Task', form=form, task=task)

@main.route('/complete_task/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = True
    task.completed_at = datetime.utcnow()
    db.session.commit()
    flash('Task marked as completed', 'success')
    return jsonify({'message': 'Task completed'})

@main.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully', 'success')
    return redirect(url_for('main.index'))
