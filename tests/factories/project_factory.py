import factory
from factory.fuzzy import FuzzyChoice
from datetime import datetime, timezone
from app.models import Project

class ProjectFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Project
        sqlalchemy_session_persistence = 'commit'
    
    name = factory.Faker('word')
    color = factory.Faker('hex_color')
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))

    @factory.post_generation
    def tasks(self, create, extracted, **kwargs):
        if not create:
            return
            
        if extracted:
            for task in extracted:
                self.tasks.append(task)
