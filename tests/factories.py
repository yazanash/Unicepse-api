import random
import uuid
import factory
from factory import fuzzy
from datetime import datetime
from src.Authentication.user_model import User
from src.Training.models.training import Training
from src.Training.models.training_program import TrainingProgram
from src.Payment.subscription_model import Subscription
from src.Payment.payment_model import Payment
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
    start_date = factory.Faker("date_time")
    end_date = factory.Faker("date_time")
    price = random.randrange(0, 1000001)
    price_ad = random.randrange(0, 1000001)
    discount_value = random.randrange(0, 1000001)
    discount_des = factory.Faker("catch_phrase")
    is_discount = factory.fuzzy.FuzzyChoice([True, False])
    is_pay = factory.fuzzy.FuzzyChoice([True, False])
    payment_total = random.randrange(0, 1000001)
    payments = []


class PaymentFactory(factory.Factory):
    """Creates fake Payments"""

    class Meta:
        model = Payment

    id = factory.Sequence(lambda n: n)
    value = random.randrange(0, 100001)
    description = factory.Faker("catch_phrase")
    date = factory.Faker("date_time")


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

