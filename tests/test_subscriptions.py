import unittest
from firebase_admin import db
from src.Payment.subscription_model import Subscription
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

    def _create_range(self, count, with_payment: bool):
        """Helper method for creating subscriptions in bulk"""
        subscriptions = []
        pl_id = SubscriptionFactory().pl_id

        for _ in range(count-1):
            subs = SubscriptionFactory()
            subs.pl_id = pl_id
            if with_payment:
                payments = []
                for _ in range(3):
                    payments.append(PaymentFactory())
                subs.payments = payments
            subs.create()
            subscriptions.append(subs)
        return subscriptions

    ######################################################################
    #  T E S T   S U B S C R I P T I O N   M O D E L
    ######################################################################

    def test_serialize_subscription(self):
        """It should serialize a subscription"""
        subs = SubscriptionFactory()

        payments = []
        for _ in range(5):
            payments.append(PaymentFactory())
        subs.payments = payments
        serialized = subs.serialize()

        self.assertEqual(serialized['id'], subs.id)
        self.assertEqual(serialized['pl_id'], subs.pl_id)
        self.assertEqual(serialized['sp_id'], subs.sp_id)
        self.assertEqual(serialized['is_pay'], subs.is_pay)
        self.assertEqual(serialized['start_date'], subs.start_date.strftime("%Y/%m/%d, %H:%M:%S"))
        self.assertEqual(serialized['end_date'], subs.end_date.strftime("%Y/%m/%d, %H:%M:%S"))
        for item in range(5):
            self.assertEqual(serialized['payments'][item]['id'], subs.payments[item].id)
            self.assertEqual(serialized['payments'][item]['value'], subs.payments[item].value)
            self.assertEqual(serialized['payments'][item]['description'], subs.payments[item].description)
            self.assertEqual(
                datetime.strptime(serialized['payments'][item]['date'], "%Y/%m/%d, %H:%M:%S"),
                subs.payments[item].date)

    def test_deserialize_subscription(self):
        """It should deserialize a subscription"""
        subs = SubscriptionFactory()

        payments = []
        for item in range(5):
            payments.append(PaymentFactory())
        subs.payments = payments

        deserialized = Subscription.deserialize(subs.serialize())
        self.assertEqual(deserialized.pl_id, subs.pl_id)
        self.assertEqual(deserialized.sp_id, subs.sp_id)
        self.assertEqual(deserialized.is_pay, subs.is_pay)
        self.assertEqual(deserialized.start_date, subs.start_date)
        self.assertEqual(deserialized.end_date, subs.end_date)
        for i in range(5):
            self.assertEqual(deserialized.payments[i].id, subs.payments[i].id)
            self.assertEqual(deserialized.payments[i].value, subs.payments[i].value)
            self.assertEqual(deserialized.payments[i].description, subs.payments[i].description)
            self.assertEqual(deserialized.payments[i].date, subs.payments[i].date)

    def test_create_subscription_no_payments(self):
        """It should create subscription with no payments"""
        subs = SubscriptionFactory()
        subs.create()
        temp_sub = Subscription.find(subs.pl_id, subs.id)
        self.assertEqual(temp_sub.sp_id, subs.sp_id)

    def test_create_subscription_with_payments(self):
        """It should create subscription with valid payments"""
        subs = SubscriptionFactory()
        payments = []
        for _ in range(3):
            payments.append(PaymentFactory())
        subs.payments = payments
        subs .create()
        temp_sub = Subscription.find(subs.pl_id, subs.id)
        self.assertEqual(temp_sub.id, subs.id)
        self.assertEqual(temp_sub.payments[0].serialize(), subs.payments[0].serialize())
        self.assertEqual(temp_sub.payments[1].serialize(), subs.payments[1].serialize())
        self.assertEqual(temp_sub.payments[2].serialize(), subs.payments[2].serialize())

    def test_read_all_subscription(self):
        """It should read all subscriptions"""
        subs_list = self._create_range(4+1, with_payment=True)
        pl_id = subs_list[0].pl_id
        temp_list = Subscription.all(pl_id)

        for i in range(4):
            self.assertEqual(temp_list[i].serialize(), subs_list[i].serialize())
