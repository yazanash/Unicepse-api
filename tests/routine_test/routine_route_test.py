import unittest

from src.gym.gym_model import Gym
from tests.factories import GymFactory, RoutineFactory
from src.common import status
from app import app
from db import db


ROUTINES_URL = "/api/v1/routines"
dt_node = "routines"

json_type = "application/json"


class TestRoutineRoutes(unittest.TestCase):
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
        db.routines.delete_many({})

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_routine(self, count):
        """Factory method to create accounts in bulk"""
        routines = []
        for _ in range(count):
            routine = RoutineFactory()
            response = self.client.post(ROUTINES_URL, json=routine.serialize())
            print(response.get_json())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Account",
            )
            routines.append(routine)
        return routines

    ######################################################################
    #  T E S T   R O U T I N E   R O U T E S
    ######################################################################
    def test_create_routine_route(self):
        """It should CREATE routine through route service"""
        routine = RoutineFactory()
        resp = self.client.post(
            ROUTINES_URL,
            json=routine.serialize(),
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_bad_request(self):
        """It should check for valid data on create route"""
        resp = self.client.post(ROUTINES_URL, json={'gym': "not enough data"}, content_type=json_type)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_read_routine_route(self):
        """It should READ gym through route service"""
        routines_list = self._create_routine(1)
        resp1 = self.client.get(f"{ROUTINES_URL}/{routines_list[0].gym_id}/{routines_list[0].pid}")
        self.assertEqual(resp1.get_json()["rid"], routines_list[0].rid)

    def test_read_bad_request(self):
        """It should check for valid id on READ gym"""
        resp = self.client.get(f"{ROUTINES_URL}/1599999")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_routine_route(self):
        """It should UPDATE gym through route service"""
        routines_list = self._create_routine(1)
        routine = routines_list[0]
        name = routine.routine_no
        routine.routine_no = "testimonial"
        resp = self.client.put(
            ROUTINES_URL,
            json=routine.serialize(),
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        response = self.client.get(f"{ROUTINES_URL}/{routine.gym_id}/{routine.pid}")
        temp = Gym.create_model()
        temp.deserialize(response.get_json())
        self.assertEqual(temp.gym_name, routine.gym_name)
        self.assertNotEqual(temp.gym_name, name)

    def test_update_bad_request(self):
        """It should check for valid data in update player"""
        self._create_routine(1)
        resp = self.client.put(
            ROUTINES_URL,
            json={'gym_name': 'not enough data'},
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_406_NOT_ACCEPTABLE)
