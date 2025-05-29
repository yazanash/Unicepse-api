import unittest

from api.src.payment.payment_model import Payment
from api.tests.factories import PaymentFactory
from src.common import status
from app import app
from db import db


PAYMENTS_URL = "/payments"
dt_node = "payments"
test_gym_id = 18

json_type = "application/json"


class TestPaymentsRoutes(unittest.TestCase):
    """Test Suite for subscription route"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""

    def setUp(self):
        """This runs before each test"""
        self.client = app.test_client()

    def tearDown(self):
        """This runs after each test"""
        db.payments.delete_many({})

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_payments(self, count):
        """Factory method to create accounts in bulk"""
        payments = []
        for _ in range(count):
            payment = PaymentFactory()
            payment.gym_id = test_gym_id
            payment.pid = 123456789
            payment.sid = 123
            response = self.client.post(PAYMENTS_URL, json=payment.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Account",
            )
            payments.append(payment)
        return payments

    ######################################################################
    #  T E S T   P L A Y E R   R O U T E S
    ######################################################################
    def test_create_payment_route(self):
        """It should CREATE payment through route service"""
        payment = PaymentFactory()
        payment.gym_id = test_gym_id
        payment.id = 10

        resp = self.client.post(
            PAYMENTS_URL,
            json=payment.serialize(),
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_bad_request(self):
        """It should check for valid data on create route"""
        resp = self.client.post(PAYMENTS_URL, json={'pay': "not enough data"}, content_type=json_type)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_read_single_subscription_route(self):
        """It should READ subscription through route service"""
        payments_list = self._create_payments(3)
        resp1 = self.client.get(f"{PAYMENTS_URL}/{payments_list[0].gym_id}/{payments_list[0].pid}/"
                                f"{payments_list[0].sid}/{payments_list[0].id}")
        self.assertEqual(resp1.get_json()["pid"], payments_list[0].pid)

        resp2 = self.client.get(f"{PAYMENTS_URL}/{payments_list[1].gym_id}/{payments_list[1].pid}/"
                                f"{payments_list[1].sid}/{payments_list[1].id}")
        self.assertEqual(resp2.get_json(), payments_list[1].serialize())

        resp3 = self.client.get(f"{PAYMENTS_URL}/{payments_list[2].gym_id}/{payments_list[2].pid}/"
                                f"{payments_list[2].sid}/{payments_list[2].id}")
        self.assertEqual(resp3.get_json(), payments_list[2].serialize())

    def test_read_payments_route(self):
        """It should READ subscription through route service"""
        payments_list = self._create_payments(5)
        resp1 = self.client.get(f"{PAYMENTS_URL}/{payments_list[0].gym_id}/{payments_list[0].pid}/"
                                f"{payments_list[0].sid}")
        print(resp1.get_json())
        for i in range(4):
            self.assertEqual(payments_list[i].serialize(), resp1.get_json()[i])

    def test_read_bad_request(self):
        """It should check for valid id on READ subscription"""
        resp = self.client.get(f"{PAYMENTS_URL}/18")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_payment_route(self):
        """It should UPDATE subscription through route service"""
        payments_list = self._create_payments(1)
        payment = payments_list[0]
        value = payment.value
        payment.value = 750000
        resp = self.client.put(
            PAYMENTS_URL,
            json=payment.serialize(),
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        response = self.client.get(f"{PAYMENTS_URL}/{payment.gym_id}/{payment.pid}/{payment.sid}/{payment.id}")
        temp = Payment.create_model()
        temp.deserialize(response.get_json())
        self.assertEqual(temp.value, payment.value)
        self.assertNotEqual(temp.value, value)

    def test_update_bad_request(self):
        """It should check for valid data in update player"""
        self._create_payments(1)
        resp = self.client.put(
            PAYMENTS_URL,
            json={'value': 'not enough data'},
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_payments_route(self):
        """It should delete payment through route service"""
        payments_list = self._create_payments(1)

        resp1 = self.client.delete(f"{PAYMENTS_URL}/{payments_list[0].gym_id}/{payments_list[0].pid}/"
                                   f"{payments_list[0].sid}/{payments_list[0].id}")

        resp2 = self.client.get(f"{PAYMENTS_URL}/{payments_list[0].gym_id}/{payments_list[0].pid}/"
                                f"{payments_list[0].sid}/{payments_list[0].id}")

        self.assertEqual(resp2.status_code, status.HTTP_204_NO_CONTENT)
