import unittest

from api.src.Authentication.profile_model import Profile
from api.tests.factories import ProfileFactory
from src.common import status
from app import app
from db import db


PROFILE_URL = "/profile"
dt_node = "profiles"
test_uid = "667f284457207891c7afb3cf"
test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiI2NjdmMjg0NDU3MjA3ODkxYzdhZmIzY2YiLCJleHAiOjE3MjczODYwODV9.XT6ksafDjnYzH58SVSR0C1xPHoOhIg0aCScOXupln_4"
json_type = "application/json"


class TestPlayerRoutes(unittest.TestCase):
    """Test Suite for player route"""

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
        db.profiles.delete_many({})

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_profiles(self, count):
        """Factory method to create profile in bulk"""
        profiles = []
        for _ in range(count):
            profile = ProfileFactory()
            profile.uid = test_uid
            response = self.client.post(PROFILE_URL, json=profile.serialize(),  headers={"x-access-token": test_token, "content_type": json_type})
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test profile",
            )
            profiles.append(profile)
        return profiles

    ######################################################################
    #  T E S T   P L A Y E R   R O U T E S
    ######################################################################
    def test_create_profile_route(self):
        """It should CREATE profile through route service"""
        profile = ProfileFactory()
        profile.uid = test_uid
        resp = self.client.post(
            PROFILE_URL,
            json=profile.serialize(),
            content_type=json_type,
            headers={"x-access-token": test_token}
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    # def test_bad_request(self):
    #     """It should check for valid data on create route"""
    #     resp = self.client.post(PROFILE_URL, json={'name': "not enough data"}, content_type=json_type)
    #     self.assertEqual(resp.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_read_profile_route(self):
        """It should READ player through route service"""
        profiles_list = self._create_profiles(1)

        resp1 = self.client.get(PROFILE_URL+"/"+test_uid,
                                content_type=json_type)
        self.assertEqual(resp1.get_json()["uid"], profiles_list[0].uid)

    # def test_read_bad_request(self):
    #     """It should check for valid id on READ player"""
    #     resp = self.client.get(PROFILE_URL, json={0: 5000})
    #     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_profile_route(self):
        """It should UPDATE profile through route service"""
        profiles_list = self._create_profiles(1)
        profile = profiles_list[0]
        full_name = profile.full_name
        profile.full_name = "testimonial"
        resp = self.client.put(
            PROFILE_URL,
            json=profile.serialize(),
            headers={"x-access-token": test_token, "content_type": json_type}
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        response = self.client.get(PROFILE_URL+"/"+test_uid)
        temp = Profile.create_model()
        temp.deserialize(response.get_json())
        self.assertEqual(temp.full_name, profile.full_name)
        self.assertNotEqual(temp.full_name, full_name)

    # def test_update_bad_request(self):
    #     """It should check for valid data in update player"""
    #     self._create_players(1)
    #     resp = self.client.put(
    #         PROFILE_URL,
    #         json={'name': 'not enough data'},
    #         content_type=json_type
    #     )
    #     self.assertEqual(resp.status_code, status.HTTP_406_NOT_ACCEPTABLE)
