import factory
from datetime import datetime
from src.Autherntication.models.user_model import User


class UserFactory(factory.Factory):
    """Creates fake Users"""
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    username = factory.Faker("name")
    password = factory.Faker("password")
    disabled = factory.FuzzyChoice([True, False])
    dateJoined = factory.LazyFunction(datetime.utcnow)
