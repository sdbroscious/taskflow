import factory
from factory.fuzzy import FuzzyChoice, FuzzyDateTime
from datetime import datetime, timedelta, timezone
from app.models import Task

class TaskFactory(factory.alchemy.SQLAlchemyModelFactory):    
    class Meta:
        model = Task
        sqlalchemy_session_persistence = 'commit'
    
    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('paragraph')
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    due_date = factory.LazyFunction(
        lambda: datetime.now(timezone.utc) + timedelta(days=30)
    )
    completed = False
    completed_at = None
    priority = FuzzyChoice([1, 2, 3, 4])  # 1: High, 2: Medium, 3: Low, 4: No Priority
    project_id = 1  # Default to first project, can be overridden
