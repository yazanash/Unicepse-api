import unittest

from src.subscription.subscription_model import Subscription
from tests.factories import SubscriptionFactory
from src.common import status
from app import app
from db import db


SUBSCRIPTION_URL = "/subscription"
dt_node = "subscription"
test_gym_id = 18

json_type = "application/json"


class TestSubscriptionsRoutes(unittest.TestCase):
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
        subscription_node = db.subscription
        subscription_node.drop()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_subscriptions(self, count):
        """Factory method to create accounts in bulk"""
        subscriptions = []
        for _ in range(count):
            subscription = SubscriptionFactory()
            subscription.gym_id = test_gym_id
            response = self.client.post(SUBSCRIPTION_URL, json=subscription.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Account",
            )
            subscriptions.append(subscription)
        return subscriptions

    ######################################################################
    #  T E S T   P L A Y E R   R O U T E S
    ######################################################################
    def test_create_subscription_route(self):
        """It should CREATE subscription through route service"""
        subscription = SubscriptionFactory()
        subscription.gym_id = test_gym_id
        print(subscription.serialize())
        resp = self.client.post(
            SUBSCRIPTION_URL,
            json=subscription.serialize(),
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_bad_request(self):
        """It should check for valid data on create route"""
        resp = self.client.post(SUBSCRIPTION_URL, json={'sport_name': "not enough data"}, content_type=json_type)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_read_single_subscription_route(self):
        """It should READ subscription through route service"""
        subscriptions_list = self._create_subscriptions(3)
        resp1 = self.client.get(f"{SUBSCRIPTION_URL}/{subscriptions_list[0].gym_id}/{subscriptions_list[0].pid}/"
                                f"{subscriptions_list[0].id}")
        self.assertEqual(resp1.get_json()["pid"], subscriptions_list[0].pid)

        resp2 = self.client.get(f"{SUBSCRIPTION_URL}/{subscriptions_list[1].gym_id}/{subscriptions_list[1].pid}/"
                                f"{subscriptions_list[1].id}")
        self.assertEqual(resp2.get_json(), subscriptions_list[1].serialize())

        resp3 = self.client.get(f"{SUBSCRIPTION_URL}/{subscriptions_list[2].gym_id}/{subscriptions_list[2].pid}/"
                                f"{subscriptions_list[2].id}")
        self.assertEqual(resp3.get_json(), subscriptions_list[2].serialize())

    def test_read_subscription_route(self):
        """It should READ subscription through route service"""
        subscriptions_list = self._create_subscriptions(3)
        resp1 = self.client.get(f"{SUBSCRIPTION_URL}/{subscriptions_list[0].gym_id}/{subscriptions_list[0].pid}")

        for i in range(4):
            self.assertEqual(subscriptions_list[i].serialize(), resp1[i])

    def test_read_bad_request(self):
        """It should check for valid id on READ subscription"""
        resp = self.client.get(f"{SUBSCRIPTION_URL}/18")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_subscription_route(self):
        """It should UPDATE subscription through route service"""
        subscriptions_list = self._create_subscriptions(1)
        subscription = subscriptions_list[0]
        sport_name = subscription.name
        subscription.sport_name = "body_building"
        resp = self.client.put(
            SUBSCRIPTION_URL,
            json=subscription.serialize(),
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        response = self.client.get(f"{SUBSCRIPTION_URL}/{subscription.gym_id}/{subscription.pid}/{subscription.id}")
        temp = Subscription.create_model()
        temp.deserialize(response.get_json())
        self.assertEqual(temp.sport_name, subscription.name)
        self.assertNotEqual(temp.sport_name, sport_name)

    def test_update_bad_request(self):
        """It should check for valid data in update player"""
        self._create_subscriptions(1)
        resp = self.client.put(
            SUBSCRIPTION_URL,
            json={'sport_name': 'not enough data'},
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_406_NOT_ACCEPTABLE)
