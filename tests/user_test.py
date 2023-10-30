import os
import unittest

import jwt

from src.common.models import DataValidationError, AuthValidationError
from . import factories
from firebase_admin import auth
from src.Authentication.models.user_model import User
# from src.common.models import database, base

users_test = []


class UserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        # database=base.reference('test')

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        User.delete_multi_users(users_test)

    def setUp(self):
        """This runs before each test"""
        # base.reference('test').delete()

    def tearDown(self):
        """This runs after each test"""
        User.delete_multi_users(users_test)

    def test_deserialize_a_user(self):
        """It should deserialize a User data and assert that it true"""
        data = {
            "uid": "0123456789",
            'username': "user1",
            'email': "user@example.com",
            'password': "secret",
            'token': "0123456789",
            'date_joined': "2021-07-27"
        }
        user = User()
        user.deserialize(data)
        self.assertEqual(user.username, data['username'])  # add assertion here

    def test_deserialize_a_user_with_key_error(self):
        """It should deserialize a User data and expect exception"""
        user = User()
        self.assertRaises(DataValidationError, user.deserialize, {})

    def test_deserialize_a_user_with_type_error(self):
        """It should deserialize a failed User data and assert that it false"""
        user = User()
        self.assertRaises(DataValidationError, user.deserialize, [])

    def test_serialize_a_user(self):
        """It should serialize a User data and assert that it true"""
        user = factories.UserFactory()
        data = user.serialize()
        self.assertEqual(data['username'], user.username)

    def test_create_a_user(self):
        """It should create a User and assert that it exist"""
        user = factories.UserFactory()
        user.create()
        self.assertIsNotNone(user.uid)  # add assertion here
        users_test.append(user.uid)

    def test_get_a_user(self):
        """It should add a User and get it to assert that it exist"""
        user = factories.UserFactory()
        # create test user
        user.create()
        users_test.append(user.uid)
        # read user data
        read_user = User.find(user.uid)
        self.assertEqual(user.email, read_user.email)  # add assertion here

    def test_update_a_user(self):
        """It should update a User and get it and assert it updated data """
        user = factories.UserFactory()
        user.create()
        users_test.append(user.uid)
        user.username = "updated user"
        updated_user = user.update()
        self.assertEqual(user.email, updated_user.email)

    def test_delete_a_user(self):
        """It should delete a User check it is deleted """
        user = factories.UserFactory()
        # create test user
        user.create()
        # read user data
        read_user = User.find(user.uid)
        self.assertEqual(user.uid, read_user.uid)  # add assertion here
        # user created successfully
        deleted_user = user.delete()
        self.assertIsNone(deleted_user)

    def test_get_all_users(self):
        """It should get all users """
        # create test user
        for i in range(10):
            user = factories.UserFactory()
            user.create()
            users_test.append(user.uid)
        # read user data

        users = User.all()
        self.assertIsNotNone(users)

    def test_is_user_exist(self):
        """It should check if a User is existed """
        user = factories.UserFactory()
        user.create()
        users_test.append(user.uid)
        user_n = User.find(user.uid)
        self.assertIsNotNone(user_n)

    def test_get_user_by_email(self):
        """It should search by user email """
        user = factories.UserFactory()
        user.create()
        users_test.append(user.uid)
        user_by_email = User.get_user_by_email(user.email)
        user_n = User.find(user.uid)
        self.assertIsNotNone(user_n)

    def test_user_login(self):
        """It should verify user credential """
        user = factories.UserFactory()
        user.create()
        users_test.append(user.uid)
        credential = {"email": user.email, "password": user.password}
        auth_user = User.get_user_by_email(credential['email'])
        token = auth_user.login_user(credential)
        data = jwt.decode(jwt=token, key=os.environ['SECRET_KEY'], algorithms='HS256')
        self.assertEqual(data['public_id'], auth_user.uid)

    def test_user_login_failed(self):
        """It should verify user credential and assert it false """
        user = factories.UserFactory()
        user.create()
        users_test.append(user.uid)
        credential = {"email": user.email, "password": "Wrong password"}
        auth_user = User.get_user_by_email(credential['email'])
        token = auth_user.login_user(credential)
        self.assertIsNone(token)
