import unittest

from src.gym.gym_model import Gym
from api.tests.factories import GymFactory
from src.common import status
from app import app
from db import db


GYMS_URL = "/api/v1/gyms"
dt_node = "gyms"

json_type = "application/json"


class TestGymRoutes(unittest.TestCase):
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
        db.gyms.delete_many({})

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_gym(self, count):
        """Factory method to create accounts in bulk"""
        gyms = []
        for _ in range(count):
            gym = GymFactory()
            response = self.client.post(GYMS_URL, json=gym.serialize())
            print(response.get_json())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Account",
            )
            gyms.append(gym)
        return gyms

    ######################################################################
    #  T E S T   G Y M   R O U T E S
    ######################################################################
    def test_create_gym_route(self):
        """It should CREATE gym through route service"""
        gym = GymFactory()
        resp = self.client.post(
            GYMS_URL,
            json=gym.serialize(),
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_bad_request(self):
        """It should check for valid data on create route"""
        resp = self.client.post(GYMS_URL, json={'gym': "not enough data"}, content_type=json_type)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_read_gyms_route(self):
        """It should READ all gyms through route service"""
        gyms_list = self._create_gym(5)
        resp1 = self.client.get(f"{GYMS_URL}")
        for i in range(4):
            self.assertEqual(gyms_list[i].serialize(), resp1.get_json()[i])

    def test_read_gym_route(self):
        """It should READ gym through route service"""
        gyms_list = self._create_gym(3)
        resp1 = self.client.get(f"{GYMS_URL}/{gyms_list[0].id}")
        self.assertEqual(resp1.get_json()["gym_name"], gyms_list[0].gym_name)

        resp2 = self.client.get(f"{GYMS_URL}/{gyms_list[1].id}")
        self.assertEqual(resp2.get_json(), gyms_list[1].serialize())

        resp3 = self.client.get(f"{GYMS_URL}/{gyms_list[2].id}")
        self.assertEqual(resp3.get_json(), gyms_list[2].serialize())

    def test_read_bad_request(self):
        """It should check for valid id on READ gym"""
        resp = self.client.get(f"{GYMS_URL}/1599999")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_gym_route(self):
        """It should UPDATE gym through route service"""
        gyms_list = self._create_gym(1)
        gym = gyms_list[0]
        name = gym.gym_name
        gym.gym_name = "testimonial"
        resp = self.client.put(
            GYMS_URL,
            json=gym.serialize(),
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        response = self.client.get(f"{GYMS_URL}/{gym.id}")
        temp = Gym.create_model()
        temp.deserialize(response.get_json())
        self.assertEqual(temp.gym_name, gym.gym_name)
        self.assertNotEqual(temp.gym_name, name)

    def test_update_bad_request(self):
        """It should check for valid data in update player"""
        self._create_gym(1)
        resp = self.client.put(
            GYMS_URL,
            json={'gym_name': 'not enough data'},
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_406_NOT_ACCEPTABLE)
