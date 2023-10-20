import random

import factory
from factory import fuzzy
from datetime import datetime
from src.Authentication.models.user_model import User
from src.Training.models.training import Training
from src.Payment.subscription import Subscription
from src.Training.models.training_program import TrainingProgram
from src.Player.player_model import Player


###################################################################
#               F A C T O R I E S
###################################################################
class UserFactory(factory.Factory):
    """Creates fake Users"""
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    username = factory.Faker("name")
    password = factory.Faker("password")
    disabled = factory.fuzzy.FuzzyChoice([True, False])
    dateJoined = factory.LazyFunction(datetime.utcnow)


class TrainingProgFactory(factory.Factory):
    class Meta:
        model = TrainingProgram

    id = factory.Sequence(lambda n: n)


class TrainingFactory(factory.Factory):
    """ Creates Fake Training Objects"""
    class Meta:
        model = Training

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")


class SubscriptionFactory(factory.Factory):
    """Creates Fake Subscriptions"""
    class Meta:
        model = Subscription

    id = factory.Sequence(lambda n: n)
    playerId = factory.Sequence(lambda n: n)
    startDate = factory.LazyFunction(datetime.utcnow())
    endDate = factory.LazyFunction(datetime.utcnow())
    price = factory.LazyAttribute(random.randrange(0, 1000001))
    priceAD = factory.LazyAttribute(random.randrange(0, 1000001))
    discountValue = factory.LazyAttribute(random.randrange(0, 1000001))
    discountDesc = factory.Faker("catch_phrase")
    isD = factory.fuzzy.FuzzyChoice([True, False])
    isPay = factory.fuzzy.FuzzyChoice([True, False])
    paymentTotal = factory.LazyAttribute(random.randrange(0, 1000001))


class PlayerFactory(factory.Factory):
    class Meta:
        model = Player

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    images = factory.Faker("email")
