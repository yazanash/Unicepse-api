import unittest
import logging
from app import app
from tests.factories import UserFactory
from src.common import status  # HTTP Status Codes
from firebase_admin import db
BASE_URL = "/auth"
content_json = "application/json"


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.logger.setLevel(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        """Runs once before test suite"""

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()

    def tearDown(self):
        """Runs once after each test case"""
        # db.reference("user").delete()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_users(self, count):
        """Factory method to create accounts in bulk"""
        users = []
        for _ in range(count):
            user = UserFactory()
            response = self.client.post(BASE_URL, json=user.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test user",
            )
            new_user = response.get_json()
            user.uid = new_user["uid"]
            users.append(user)
        return users

    def test_index(self):
        """It should get 200_OK from the Home Page"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_a_user(self):
        """It should return status code 201 user created successfully"""
        user = UserFactory()
        response = self.client.post(BASE_URL,
                                    json=user.serialize(),
                                    content_type=content_json
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_a_user(self):
        """It should return status code 200 and return user data"""
        user = self._create_users(1)[0]
        resp = self.client.get(
            f"{BASE_URL}/{user.uid}", content_type=content_json
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["username"], user.username)

    def test_get_user_not_found(self):
        """It should return status code 200 and return user data"""
        resp = self.client.get(
            f"{BASE_URL}/789654123", content_type=content_json
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user(self):
        """It should return status code 200 and update user data"""
        user = UserFactory()
        # create user
        user.uid = 123456789
        response = self.client.post(BASE_URL, json=user.serialize(), content_type=content_json)
        user.deserialize(response.get_json())
        user.username = "User Number 3"
        resp = self.client.put(
            f"{BASE_URL}/{user.uid}", json=user.serialize(), content_type=content_json
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json()['username'], user.username)

    def test_update_user_not_found(self):
        """It should return status code 200 and return user data"""
        # user = self._create_users(1)[0]
        resp = self.client.put(
            f"{BASE_URL}/565656565", content_type=content_json
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_users_list(self):
        """It should Get a list of Accounts"""
        self._create_users(5)
        resp = self.client.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertGreater(len(data), 0)
