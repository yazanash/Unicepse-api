import os
import unittest
import logging

import jwt

from tests.factories import UserFactory
from src.common import status  # HTTP Status Codes
from app import app
from db import db
BASE_URL = "/auth"
content_json = "application/json"

users_test = []
test_password = "123456789"


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
        db.Users.delete_many({})

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
            users_test.append(user)
        return users

    def _create_users_with_password(self):
        """Factory method to create accounts in bulk"""
        user = UserFactory()
        user.password = test_password
        response = self.client.post(BASE_URL, json=user.serialize())
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            "Could not create test user",
        )
        new_user = response.get_json()
        user.uid = new_user["uid"]
        users_test.append(user)
        return user
    # # def test_index(self):
    # #     """It should get 200_OK from the Home Page"""
    # #     response = self.client.get('/')
    # #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #

    def test_create_a_user(self):
        """It should return status code 201 user created successfully"""
        user = UserFactory()
        response = self.client.post(BASE_URL,
                                    json=user.serialize(),
                                    content_type=content_json
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.get_json()
        users_test.append(data['uid'])

    # def test_verify_otp(self):
    #     """It should return status code 200 user verified successfully"""
    #     email = "yazan.ash.doonaas@gmail.com"
    #     ver = db.emails.find_one({"email": email})
    #     response = self.client.post(BASE_URL+"/verify",
    #                                 json={"email": email, "otp": ver["otp"]},
    #                                 content_type=content_json
    #                                 )
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

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
        """It should return status code 404 for not existing user"""
        resp = self.client.get(
            f"{BASE_URL}/asdfghytrew23456789iuytree", content_type=content_json
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user(self):
        """It should return status code 200 and update user data"""
        user = UserFactory()
        # create user
        response = self.client.post(BASE_URL, json=user.serialize(), content_type=content_json)
        data = response.get_json()
        user.deserialize(response.get_json())
        user.uid = data['uid']
        users_test.append(user.uid)
        user.username = "User Number 3"
        resp = self.client.put(
            f"{BASE_URL}/{user.uid}", json=user.serialize(), content_type=content_json
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json()['username'], user.username)

    def test_update_user_not_found(self):
        """It should return status code 404 for update for not exist user"""
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

    def test_login_user(self):
        """It should verify cred"""
        user = self._create_users_with_password()
        resp = self.client.post(f"{BASE_URL}/login",
                                json={"email": user.email,
                                      'password': test_password},
                                content_type=content_json)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        token_val = jwt.decode(jwt=data, key=os.environ["SECRET_KEY"], algorithms="HS256")
        self.assertEqual(token_val['public_id'], user.uid)
