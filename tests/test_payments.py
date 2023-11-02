import unittest
from firebase_admin import db
from src.payment.payment_model import Payment
from .factories import SubscriptionFactory, PaymentFactory
from datetime import datetime


dt_node = "TestSubscription"


class TestPayments(unittest.TestCase):
    """ Test Suite for Subscription Model """

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        # Player.dt_name = dt_node

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.reference(dt_node).delete()
        Payment.dt_name = "Subscriptions"

    def setUp(self):
        """This runs before each test"""
        Payment.dt_name = dt_node
        db.reference(dt_node).delete()

    def tearDown(self):
        """This runs after each test"""
        db.reference(dt_node).delete()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_range(self, count):
        """Helper method for creating payments in bulk
        """
        payments = []
        pl_id = SubscriptionFactory().pl_id
        sub_id = SubscriptionFactory().id
        for _ in range(count-1):
            pays = PaymentFactory()
            pays.pl_id = pl_id
            pays.sub_id = sub_id
            pays.create()
            payments.append(pays)
        return payments

    ######################################################################
    #  T E S T   P A Y M E N T   M O D E L
    ######################################################################

    def test_serialize_payment(self):
        """It should serialize a subscription"""
        pays = PaymentFactory()
        serialized = pays.serialize()

        self.assertEqual(serialized['id'], pays.id)
        self.assertEqual(serialized['pl_id'], pays.pl_id)
        self.assertEqual(serialized['sub_id'], pays.sub_id)
        self.assertEqual(serialized['value'], pays.value)
        self.assertEqual(serialized['description'], pays.description)
        self.assertEqual(serialized['date'], pays.date.strftime("%Y/%m/%d, %H:%M:%S"))

    def test_deserialize_payment(self):
        """It should deserialize a payment"""
        pays = PaymentFactory()
        deserialized = Payment.deserialize(pays.serialize())
        self.assertEqual(deserialized.pl_id, pays.pl_id)
        self.assertEqual(deserialized.sub_id, pays.sub_id)
        self.assertEqual(deserialized.value, pays.value)
        self.assertEqual(deserialized.description, pays.description)
        self.assertEqual(deserialized.date, pays.date)

    def test_create_payment(self):
        """It should create subscription with no payments"""
        payment = PaymentFactory()
        payment.create()
        temp_pay = Payment.find(payment.pl_id, payment.sub_id, payment.id)
        self.assertEqual(temp_pay.value, payment.value)

    def test_read_all_payments(self):
        """It should read all subscriptions"""
        pays_list = self._create_range(4+1)
        pl_id = pays_list[0].pl_id
        sub_id = pays_list[0].sub_id
        temp_list = Payment.all(pl_id,sub_id)

        for i in range(4):
            self.assertEqual(temp_list[i].serialize(), pays_list[i].serialize())

    def test_update_payment(self):
        """It should update subscription """
        pays = PaymentFactory()
        pays.create()
        pays.value = 15000
        pays.update()
        temp_sub = Payment.find(pays.pl_id, pays.sub_id, pays.id)
        self.assertEqual(temp_sub.value, 15000)

    def test_delete_payment(self):
        """It should delete subscription"""
        pays = PaymentFactory()
        pays.create()
        pays.delete()
        temp_sub = Payment.find(pays.pl_id, pays.sub_id, pays.id)
        self.assertIsNone(temp_sub)
