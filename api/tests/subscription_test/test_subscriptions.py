import unittest

from src.subscription.subscription_model import Subscription
from api.tests.factories import SubscriptionFactory
from db import db


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
        db.subscriptions.delete_many({})

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_range(self, count):
        """Helper method for creating subscriptions in bulk
        """
        subscriptions = []
        fake_sub = SubscriptionFactory()
        pid = fake_sub.pid
        gym_id = fake_sub.gym_id

        for _ in range(count-1):
            subs = SubscriptionFactory()
            subs.pid = pid
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
        self.assertEqual(serialized['pid'], subs.pid)
        self.assertEqual(serialized['gym_id'], subs.gym_id)
        self.assertEqual(serialized['sport_name'], subs.sport_name)
        self.assertEqual(serialized['is_paid'], subs.is_paid)
        self.assertEqual(serialized['start_date'], subs.start_date.strftime("%Y/%m/%d, %H:%M:%S"))
        self.assertEqual(serialized['end_date'], subs.end_date.strftime("%Y/%m/%d, %H:%M:%S"))

    def test_deserialize_subscription(self):
        """It should deserialize a subscription"""
        subs = SubscriptionFactory()
        deserialized = Subscription.create_model()
        deserialized.deserialize(subs.serialize())
        self.assertEqual(deserialized.pid, subs.pid)
        self.assertEqual(deserialized.gym_id, subs.gym_id)
        self.assertEqual(deserialized.sport_name, subs.sport_name)
        self.assertEqual(deserialized.is_paid, subs.is_paid)
        self.assertEqual(deserialized.start_date, subs.start_date)
        self.assertEqual(deserialized.end_date, subs.end_date)

    def test_create_subscription(self):
        """It should create subscription with no payments"""
        subs = SubscriptionFactory()
        subs.create()
        temp_sub = Subscription.find(subs.gym_id, subs.pid, subs.id)
        self.assertEqual(temp_sub.id, subs.id)
        self.assertEqual(temp_sub.sport_name, subs.sport_name)
        self.assertEqual(temp_sub.pid, subs.pid)
        self.assertEqual(temp_sub.gym_id, subs.gym_id)
        self.assertEqual(temp_sub.start_date, subs.start_date)

    def test_read_all_subscription(self):
        """It should read all subscriptions"""
        subs_list = self._create_range(4+1)
        pid = subs_list[0].pid
        gym_id = subs_list[0].gym_id
        temp_list = Subscription.all(gym_id, pid)

        for i in range(4):
            self.assertEqual(temp_list[i].serialize(), subs_list[i].serialize())

    def test_update_subscription(self):
        """It should update subscription """
        subs = SubscriptionFactory()
        subs.create()
        subs.price = 15000
        subs.update()
        temp_sub = Subscription.find(subs.gym_id, subs.pid, subs.id)
        self.assertEqual(temp_sub.price, 15000)
