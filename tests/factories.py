import random
import uuid
import factory
from factory import fuzzy
from datetime import datetime
from src.Authentication.user_model import User
from src.subscription.subscription_model import Subscription
from src.payment.payment_model import Payment
from src.Player.player_model import Player
from src.metrics.metrics_model import Metric
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


# class TrainingProgFactory(factory.Factory):
#     class Meta:
#         model = TrainingProgram
#
#     id = factory.Sequence(lambda n: n)
#     name = factory.Faker("name")
#     training_list = ['train1', 'train2']
#     provider = factory.Faker("name")
#
#
# class TrainingFactory(factory.Factory):
#     """ Creates Fake Training Objects"""
#     class Meta:
#         model = Training
#
#     id = factory.Sequence(lambda n: n)
#     name = factory.Faker("name")
#     rounds = factory.fuzzy.FuzzyInteger(1, 15)
#     image_url = factory.Faker("email")
#

def pays():
    return [PaymentFactory() for i in range(2)]


class SubscriptionFactory(factory.Factory):
    """Creates Fake Subscriptions"""
    class Meta:
        model = Subscription

    id = factory.Sequence(lambda n: n)
    pl_id = factory.Sequence(lambda n: n)
    gym_id = factory.Sequence(lambda n: n)
    sport_name = factory.Faker("user_name")
    trainer_name = factory.Faker("user_name")
    start_date = factory.Faker("date_time")
    end_date = factory.Faker("date_time")
    price = random.randrange(0, 1000001)
    discount_value = random.randrange(0, 1000001)
    discount_des = factory.Faker("catch_phrase")
    is_payed = factory.fuzzy.FuzzyChoice([True, False])
    list_of_payments = None


class PaymentFactory(factory.Factory):
    """Creates fake Payments"""

    class Meta:
        model = Payment

    id = factory.Sequence(lambda n: n)
    pl_id = factory.Sequence(lambda n: n)
    sub_id = factory.Sequence(lambda n: n)
    gym_id = factory.Sequence(lambda n: n)
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
    date_of_birth = fuzzy.FuzzyInteger(1999, 2024)
    gender = fuzzy.FuzzyChoice(["male", 'female'])
    balance = random.randrange(0, 100000)


class MetricsFactory(factory.Factory):

    class Meta:
        model = Metric

    id = factory.Sequence(lambda n: n)
    pl_id = factory.Sequence(lambda n: n)
    gym_id = factory.Sequence(lambda n: n)
    height = factory.Sequence(lambda n: n)
    weight = factory.Sequence(lambda n: n)
    l_arm = factory.Sequence(lambda n: n)
    r_arm = factory.Sequence(lambda n: n)
    l_humerus = factory.Sequence(lambda n: n)
    r_humerus = factory.Sequence(lambda n: n)
    l_thigh = factory.Sequence(lambda n: n)
    r_thigh = factory.Sequence(lambda n: n)
    l_leg = factory.Sequence(lambda n: n)
    r_leg = factory.Sequence(lambda n: n)
    neck = factory.Sequence(lambda n: n)
    shoulders = factory.Sequence(lambda n: n)
    waist = factory.Sequence(lambda n: n)
    chest = factory.Sequence(lambda n: n)
    hips = factory.Sequence(lambda n: n)
    check_date = factory.Faker("date_time")
