import unittest

from src.common.models import DataValidationError
from . import factories
from firebase_admin import db
from src.Authentication.models.user_model import User
# from src.common.models import database, base

data_node = "user"


class UserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        # database=base.reference('test')

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""

    def setUp(self):
        """This runs before each test"""
        # base.reference('test').delete()

    def tearDown(self):
        """This runs after each test"""
        db.reference(data_node).delete()

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
        user.dt_name = data_node
        user.create()
        self.assertIsNotNone(user.uid)  # add assertion here

    def test_get_a_user(self):
        """It should add a User and get it to assert that it exist"""

        user = factories.UserFactory()
        User.dt_name = data_node
        # create test user
        user.create()
        # read user data
        read_user = User.find(user.uid)
        self.assertEqual(user.username, read_user.username)  # add assertion here

    def test_update_a_user(self):
        """It should update a User and get it and assert it updated data """
        user = factories.UserFactory()
        User.dt_name = data_node
        # create test user
        user.create()
        # read user data
        read_user = User.find(user.uid)
        self.assertEqual(user.username, read_user.username)  # add assertion here
        # user created successfully
        user.username = "updated user"
        user.update()
        read_user = User.find(user.uid)
        self.assertEqual(user.username, read_user.username)

    def test_delete_a_user(self):
        """It should delete a User check it is deleted """
        user = factories.UserFactory()
        User.dt_name = data_node
        # create test user
        user.create()
        # read user data
        read_user = User.find(user.uid)
        self.assertEqual(user.username, read_user.username)  # add assertion here
        # user created successfully
        user.delete()
        read_user = User.check_if_exist(user.uid)
        self.assertIsNone(read_user)

    def test_get_all_users(self):
        """It should get all users """
        # create test user
        for i in range(10):
            user = factories.UserFactory()
            user.create()
        # read user data

        users = User.all()
        self.assertIsNotNone(users)

    def test_is_user_exist(self):
        """It should check if a User is existed """
        user = factories.UserFactory()
        user.dt_name = data_node
        user.uid = 256365453
        user_n = User.find(user.uid)
        self.assertIsNone(user_n)
