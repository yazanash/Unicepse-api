import unittest

from src.subscription.subscription_model import Subscription
from .factories import SubscriptionFactory, PaymentFactory


class TestSubscriptions(unittest.TestCase):
    """ Test Suite for Subscription Model """

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""

    def setUp(self):
        """This runs before each test"""

    def tearDown(self):
        """This runs after each test"""

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_range(self, count):
        """Helper method for creating subscriptions in bulk
        """
        subscriptions = []
        fakeSub = SubscriptionFactory()
        pl_id = fakeSub.pl_id
        gym_id = fakeSub.gym_id

        for _ in range(count-1):
            subs = SubscriptionFactory()
            subs.pl_id = pl_id
            subs.gym_id = gym_id
            subs.create()
            subscriptions.append(subs)
        return subscriptions

    ######################################################################
    #  T E S T   S U B S C R I P T I O N   M O D E L
    ######################################################################

    def test_serialize_subscription(self):
        """It should serialize a subscription"""
        subs = SubscriptionFactory()
        serialized = subs.serialize()

        self.assertEqual(serialized['id'], subs.id)
        self.assertEqual(serialized['pl_id'], subs.pl_id)
        self.assertEqual(serialized['gym_id'], subs.gym_id)
        self.assertEqual(serialized['sport_name'], subs.sport_name)
        self.assertEqual(serialized['is_payed'], subs.is_payed)
        self.assertEqual(serialized['start_date'], subs.start_date.strftime("%Y/%m/%d, %H:%M:%S"))
        self.assertEqual(serialized['end_date'], subs.end_date.strftime("%Y/%m/%d, %H:%M:%S"))

    def test_deserialize_subscription(self):
        """It should deserialize a subscription"""
        subs = SubscriptionFactory()
        deserialized = Subscription.deserialize(subs.serialize())
        self.assertEqual(deserialized.pl_id, subs.pl_id)
        self.assertEqual(deserialized.gym_id, subs.gym_id)
        self.assertEqual(deserialized.sport_name, subs.sport_name)
        self.assertEqual(deserialized.is_payed, subs.is_payed)
        self.assertEqual(deserialized.start_date, subs.start_date)
        self.assertEqual(deserialized.end_date, subs.end_date)

    def test_create_subscription(self):
        """It should create subscription with no payments"""
        subs = SubscriptionFactory()
        subs.create()
        temp_sub = Subscription.find(subs.gym_id, subs.pl_id, subs.id)
        self.assertEqual(temp_sub.id, subs.id)
        self.assertEqual(temp_sub.sport_name, subs.sport_name)
        self.assertEqual(temp_sub.pl_id, subs.pl_id)
        self.assertEqual(temp_sub.gym_id, subs.gym_id)
        self.assertEqual(temp_sub.start_date, subs.start_date)

    def test_read_all_subscription(self):
        """It should read all subscriptions"""
        subs_list = self._create_range(4+1)
        pl_id = subs_list[0].pl_id
        gym_id = subs_list[0].gym_id
        temp_list = Subscription.all(gym_id, pl_id)

        for i in range(4):
            self.assertEqual(temp_list[i].serialize(), subs_list[i].serialize())

    def test_update_subscription(self):
        """It should update subscription """
        subs = SubscriptionFactory()
        subs.create()
        subs.price = 15000
        subs.update()
        temp_sub = Subscription.find(subs.gym_id, subs.pl_id, subs.id)
        self.assertEqual(temp_sub.price, 15000)

    def test_delete_subscription(self):
        """It should delete subscription"""
        subs = SubscriptionFactory()
        subs.create()
        subs.delete()
        temp_sub = Subscription.find(subs.gym_id, subs.pl_id, subs.id)
        self.assertIsNone(temp_sub)
