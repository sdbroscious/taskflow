from . import db
from datetime import datetime
from . import db

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.Integer, default=4)  # 1: High, 2: Medium, 3: Low, 4: No Priority
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)

    @property
    def priority_label(self):
        """Return a human-readable label for the task priority."""
        priority_map = {
            1: 'High',
            2: 'Medium',
            3: 'Low',
            4: 'No Priority'
        }
        return priority_map.get(self.priority, 'Unknown')

    def __repr__(self):
        return f'<Task {self.title}>'

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(7), default='#000000')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tasks = db.relationship('Task', backref='project', lazy='dynamic')

    def __repr__(self):
        return f'<Project {self.name}>'
