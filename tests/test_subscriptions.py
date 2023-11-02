import unittest
from firebase_admin import db
from src.subscription.subscription_model import Subscription
from .factories import SubscriptionFactory, PaymentFactory
from datetime import datetime


dt_node = "TestSubscription"


class TestSubscriptions(unittest.TestCase):
    """ Test Suite for Subscription Model """

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        # Player.dt_name = dt_node

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.reference(dt_node).delete()
        Subscription.dt_name = "Subscriptions"

    def setUp(self):
        """This runs before each test"""
        Subscription.dt_name = dt_node
        db.reference(dt_node).delete()

    def tearDown(self):
        """This runs after each test"""
        db.reference(dt_node).delete()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_range(self, count):
        """Helper method for creating subscriptions in bulk
        """
        subscriptions = []
        pl_id = SubscriptionFactory().pl_id

        for _ in range(count-1):
            subs = SubscriptionFactory()
            subs.pl_id = pl_id
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
        self.assertEqual(serialized['sp_id'], subs.sp_id)
        self.assertEqual(serialized['is_pay'], subs.is_pay)
        self.assertEqual(serialized['start_date'], subs.start_date.strftime("%Y/%m/%d, %H:%M:%S"))
        self.assertEqual(serialized['end_date'], subs.end_date.strftime("%Y/%m/%d, %H:%M:%S"))

    def test_deserialize_subscription(self):
        """It should deserialize a subscription"""
        subs = SubscriptionFactory()
        deserialized = Subscription.deserialize(subs.serialize())
        self.assertEqual(deserialized.pl_id, subs.pl_id)
        self.assertEqual(deserialized.sp_id, subs.sp_id)
        self.assertEqual(deserialized.is_pay, subs.is_pay)
        self.assertEqual(deserialized.start_date, subs.start_date)
        self.assertEqual(deserialized.end_date, subs.end_date)

    def test_create_subscription(self):
        """It should create subscription with no payments"""
        subs = SubscriptionFactory()
        subs.create()
        temp_sub = Subscription.find(subs.pl_id, subs.id)
        self.assertEqual(temp_sub.sp_id, subs.sp_id)

    def test_read_all_subscription(self):
        """It should read all subscriptions"""
        subs_list = self._create_range(4+1)
        pl_id = subs_list[0].pl_id
        temp_list = Subscription.all(pl_id)

        for i in range(4):
            self.assertEqual(temp_list[i].serialize(), subs_list[i].serialize())

    def test_update_subscription(self):
        """It should update subscription """
        subs = SubscriptionFactory()
        subs.create()
        subs.price = 15000
        subs.update()
        temp_sub = Subscription.find(subs.pl_id, subs.id)
        self.assertEqual(temp_sub.price, 15000)

    def test_delete_subscription(self):
        """It should delete subscription"""
        subs = SubscriptionFactory()
        subs.create()
        subs.delete()
        temp_sub = Subscription.find(subs.pl_id, subs.id)
        self.assertIsNone(temp_sub)
