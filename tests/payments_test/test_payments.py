import unittest
from db import db
from src.payment.payment_model import Payment
from tests.factories import PaymentFactory

sids = []


class TestPayments(unittest.TestCase):
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
        db.payments.delete_many({})

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_range(self, count):
        """Helper method for creating payments in bulk
        """
        payments = []
        for _ in range(count):
            pays = PaymentFactory()
            pays.pid = 123456789
            pays.sid = 123
            pays.gym_id = 18
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
        self.assertEqual(serialized['pid'], pays.pid)
        self.assertEqual(serialized['sid'], pays.sid)
        self.assertEqual(serialized['value'], pays.value)
        self.assertEqual(serialized['description'], pays.description)
        self.assertEqual(serialized['date'], pays.date.strftime("%d/%m/%Y"))

    def test_deserialize_payment(self):
        """It should deserialize a payment"""
        pays = PaymentFactory()
        deserialized = Payment.create_model()
        deserialized.deserialize(pays.serialize())
        print(deserialized.serialize())
        self.assertEqual(deserialized.pid, pays.pid)
        self.assertEqual(deserialized.sid, pays.sid)
        self.assertEqual(deserialized.value, pays.value)
        self.assertEqual(deserialized.description, pays.description)
        self.assertEqual(deserialized.date.strftime("%d/%m/%Y"), pays.date.strftime("%d/%m/%Y"))

    def test_create_payment(self):
        """It should create subscription with no payments"""
        payment = PaymentFactory()
        payment.create()
        temp_pay = Payment.find(payment.gym_id, payment.pid, payment.sid, payment.id)
        self.assertEqual(temp_pay.value, payment.value)

    def test_read_all_payments(self):
        """It should read all subscriptions"""
        pays_list = self._create_range(5)
        pid = pays_list[0].pid
        sid = pays_list[0].sid
        gym_id = pays_list[0].gym_id
        temp_list = Payment.all(gym_id, pid, sid)
        for i in range(4):
            self.assertEqual(temp_list[i].serialize(), pays_list[i].serialize())

    def test_update_payment(self):
        """It should update subscription """
        pays = PaymentFactory()
        pays.create()
        sids.append(pays.sid)
        pays.value = 15000
        pays.update()
        temp_sub = Payment.find(pays.gym_id, pays.pid, pays.sid, pays.id)
        self.assertEqual(temp_sub.value, 15000)

    def test_delete_payment(self):
        """It should delete subscription"""
        pays = PaymentFactory()
        pays.create()
        pays.delete()
        temp_sub = Payment.find(pays.gym_id, pays.pid, pays.sid, pays.id)
        self.assertIsNone(temp_sub)
