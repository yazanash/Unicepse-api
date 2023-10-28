import random
import uuid
import factory
from factory import fuzzy
from datetime import datetime
from src.Authentication.models.user_model import User
from src.Training.models.training import Training
from src.Payment.subscription import Subscription
from src.Training.models.training_program import TrainingProgram
from src.Player.player_model import Player
from src.common.utils import TokenGenerator


###################################################################
#               F A C T O R I E S
###################################################################
class UserFactory(factory.Factory):
    """Creates fake Users"""
    class Meta:
        model = User

    uid = uuid.uuid4().hex
    username = factory.Faker("name")
    password = factory.Faker("password")
    email = factory.Faker("email")
    token = factory.LazyFunction(TokenGenerator.generate_token)
    date_joined = factory.LazyFunction(datetime.utcnow)


class TrainingProgFactory(factory.Factory):
    class Meta:
        model = TrainingProgram

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    training_list = ['train1', 'train2']
    provider = factory.Faker("name")


class TrainingFactory(factory.Factory):
    """ Creates Fake Training Objects"""
    class Meta:
        model = Training

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    rounds = factory.fuzzy.FuzzyInteger(1, 15)
    image_url = factory.Faker("email")


class SubscriptionFactory(factory.Factory):
    """Creates Fake Subscriptions"""
    class Meta:
        model = Subscription

    id = factory.Sequence(lambda n: n)
    pl_id = factory.Sequence(lambda n: n)
    sp_id = factory.Sequence(lambda n: n)
    tr_id = factory.Sequence(lambda n: n)
    startDate = factory.Faker("date_object")
    endDate = factory.Faker("date_object")
    price = random.randrange(0, 1000001)
    priceAD = random.randrange(0, 1000001)
    discountValue = random.randrange(0, 1000001)
    discountDes = factory.Faker("catch_phrase")
    isD = factory.fuzzy.FuzzyChoice([True, False])
    isPay = factory.fuzzy.FuzzyChoice([True, False])
    paymentTotal = random.randrange(0, 1000001)


class PlayerFactory(factory.Factory):
    class Meta:
        model = Player

    pid = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    width = fuzzy.FuzzyFloat(10, 100)
    height = fuzzy.FuzzyFloat(10, 100)
    date_of_birth = factory.Faker("date_time")
    gender = fuzzy.FuzzyChoice(["male", 'female'])
    balance = random.randrange(0, 100000)

