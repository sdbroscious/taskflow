import factory
from factory import Faker
from factory.alchemy import SQLAlchemyModelFactory
from datetime import datetime, timedelta, timezone

from app import db
from app.models import Task, Project

class BaseFactory(SQLAlchemyModelFactory):
    """Base factory with common configuration."""
    
    class Meta:
        abstract = True
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

class ProjectFactory(BaseFactory):
    """Factory for Project model."""
    
    class Meta:
        model = Project
    
    name = Faker('sentence', nb_words=3)
    color = Faker('hex_color')
    created_at = factory.LazyFunction(datetime.utcnow)

class TaskFactory(BaseFactory):
    """Factory for Task model."""
    
    class Meta:
        model = Task
    
    title = Faker('sentence', nb_words=4)
    description = Faker('paragraph')
    due_date = factory.LazyFunction(lambda: datetime.utcnow() + timedelta(days=7))
    priority = factory.Iterator([1, 2, 3])  # 1: High, 2: Medium, 3: Low
    completed = False
    created_at = factory.LazyFunction(datetime.utcnow)
    project = factory.SubFactory(ProjectFactory)
