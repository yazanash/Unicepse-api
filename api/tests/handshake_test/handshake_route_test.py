import unittest

from api.tests.factories import HandShakeFactory
from src.common import status
from app import app
from db import db


HANDSHAKES_URL = "/api/v1/handshake"
dt_node = "handshake"
test_gym_id = 18

json_type = "application/json"


class TestHandShakeRoutes(unittest.TestCase):
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
        db.handshakes.delete_many({})

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_hand_shake(self, count):
        """Factory method to create accounts in bulk"""
        handshakes = []
        for _ in range(count):
            handshake = HandShakeFactory()
            response = self.client.post(HANDSHAKES_URL, json=handshake.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Account",
            )
            handshakes.append(handshake)
        return handshakes

    ######################################################################
    #  T E S T   H A N D S H A K E   R O U T E S
    ######################################################################
    def test_create_hand_shake_route(self):
        """It should CREATE payment through route service"""
        handshake = HandShakeFactory()
        resp = self.client.post(
            HANDSHAKES_URL,
            json=handshake.serialize(),
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_bad_request(self):
        """It should check for valid data on create route"""
        resp = self.client.post(HANDSHAKES_URL, json={'HAND': "not enough data"}, content_type=json_type)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_read_hand_shakes_route(self):
        """It should READ subscription through route service"""
        handshakes_list = self._create_hand_shake(5)
        resp1 = self.client.get(f"{HANDSHAKES_URL}/{handshakes_list[0].uid}")
        print(resp1.get_json())
        for i in range(4):
            print(resp1.get_json()[i])
            print(handshakes_list[i].serialize())
            self.assertEqual(handshakes_list[i].serialize(), resp1.get_json()[i])


