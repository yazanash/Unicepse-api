import random
import uuid
import factory
from factory import fuzzy
from datetime import datetime

from api.src.Authentication.profile_model import Profile
from src.Authentication.user_model import User
from src.attedence.attendance_model import Attendance
from src.offer.offer_model import Offer
from src.gym.gym_model import Gym
from src.handshake.handshake_model import HandShake
from src.license.license_model import License
from src.plans.plan_model import Plan
from src.routine.routine_model import Routine
from src.subscription.subscription_model import Subscription
from api.src.payment.payment_model import Payment
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


class ProfileFactory(factory.Factory):
    """Creates fake Profiles"""
    class Meta:
        model = Profile

    full_name = factory.Faker("name")
    phone = "+963994916917"
    birth_date = fuzzy.FuzzyInteger(1999, 2024)
    gender_male = fuzzy.FuzzyChoice([True, False])
    weight = fuzzy.FuzzyFloat(10, 100)
    height = fuzzy.FuzzyFloat(10, 100)


def pays():
    return [PaymentFactory() for i in range(2)]


class SubscriptionFactory(factory.Factory):
    """Creates Fake Subscriptions"""
    class Meta:
        model = Subscription

    id = factory.Sequence(lambda n: n)
    pid = factory.Sequence(lambda n: n)
    gym_id = factory.Sequence(lambda n: n)
    sport_name = factory.Faker("user_name")
    trainer_name = factory.Faker("user_name")
    start_date = factory.Faker("date_time")
    end_date = factory.Faker("date_time")
    price = random.randrange(0, 1000001)
    discount_value = random.randrange(0, 1000001)
    discount_des = factory.Faker("catch_phrase")
    is_paid = factory.fuzzy.FuzzyChoice([True, False])
    paid_value = random.randrange(0, 1000001)
    payments = None


class PaymentFactory(factory.Factory):
    """Creates fake Payments"""

    class Meta:
        model = Payment

    id = factory.Sequence(lambda n: n)
    pid = 123456789
    sid = 123
    gym_id = 18
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
    pid = factory.Sequence(lambda n: n)
    gym_id = factory.Sequence(lambda n: n)
    height = fuzzy.FuzzyFloat(10, 100)
    weight = fuzzy.FuzzyFloat(10, 100)
    l_arm = fuzzy.FuzzyFloat(10, 100)
    r_arm = fuzzy.FuzzyFloat(10, 100)
    l_humerus = fuzzy.FuzzyFloat(10, 100)
    r_humerus = fuzzy.FuzzyFloat(10, 100)
    l_thigh = fuzzy.FuzzyFloat(10, 100)
    r_thigh = fuzzy.FuzzyFloat(10, 100)
    l_leg = fuzzy.FuzzyFloat(10, 100)
    r_leg = fuzzy.FuzzyFloat(10, 100)
    neck = fuzzy.FuzzyFloat(10, 100)
    shoulders = fuzzy.FuzzyFloat(10, 100)
    waist = fuzzy.FuzzyFloat(10, 100)
    chest = fuzzy.FuzzyFloat(10, 100)
    hips = fuzzy.FuzzyFloat(10, 100)
    check_date = factory.Faker("date_time")


class HandShakeFactory(factory.Factory):
    """Creates fake Payments"""

    class Meta:
        model = HandShake

    pid = random.randrange(1000000, 10000100)
    uid = 123456789
    gym_id = 18


class GymFactory(factory.Factory):
    """Creates fake Payments"""

    class Meta:
        model = Gym

    id = factory.Sequence(lambda n: n)
    gym_name = factory.Faker("name")
    owner_name = factory.Faker("name")
    phone_number = "+963994916917"
    telephone = "016235658"
    logo = factory.Faker("url")
    address = fuzzy.FuzzyText()


class LicenseFactory(factory.Factory):
    """Creates fake license"""

    class Meta:
        model = License

    gym_id = 18
    plan_id = random.randrange(0, 12)
    price = random.randrange(0, 100001)
    subscribe_date = factory.Faker("date_time")
    period = random.randrange(1, 12)


class PlanFactory(factory.Factory):
    """Creates fake plans"""

    class Meta:
        model = Plan

    plan_name = factory.Faker("name")
    price = random.randrange(0, 100001)
    period = random.randrange(1, 12)
    description = factory.Faker("catch_phrase")


class OfferFactory(factory.Factory):
    """Creates fake offer"""

    class Meta:
        model = Offer

    offer_name = factory.Faker("name")
    offer_percent = random.randrange(0, 100)
    period = random.randrange(1, 12)
    description = factory.Faker("catch_phrase")


class AttendanceFactory(factory.Factory):
    """Creates fake attendance """

    class Meta:
        model = Attendance

    aid = random.randrange(0, 10000)
    date = datetime.now().strftime("%d/%m/%Y")
    login_time = datetime.now().strftime("%M:%H")
    logout_time = datetime.now().strftime("%M:%H")
    pid = "123456789"
    sid = "123456789454"
    gym_id = "18"


class RoutineFactory(factory.Factory):
    """Creates fake attendance """

    class Meta:
        model = Routine

    rid = random.randrange(0, 100)
    pid = 123456789
    gym_id = 18
    routine_no = factory.Faker("catch_phrase")
    routine_date = login_time = factory.Faker("date_time")
    days_group_map = [{random.randrange(1, 6): factory.Faker("catch_phrase")} for n in range(5)]
    routine_items = [
        {
            "id": 118,
            "ExerciseName":  factory.Faker("catch_phrase"),
            "ExerciseImage": random.randrange(1, 5),
            "Muscle_Group": random.randrange(1, 8),
            "orders": factory.Faker("catch_phrase"),
            "notes": factory.Faker("catch_phrase"),
            "itemOrder": 1
        } for i in range(8)]
