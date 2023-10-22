import unittest


from src.Authentication.models.user_model import User
# from src.common.models import database, base


class UserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        # database=base.reference('test')

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        # database = base.reference('user')

    def setUp(self):
        """This runs before each test"""
        # base.reference('test').delete()

    def tearDown(self):
        """This runs after each test"""
        # db.session.remove()

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

    def test_serialize_a_user(self):
        """It should serialize a User data and assert that it true"""
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
        user.serialize()
        self.assertEqual(data['username'], user.username)  # add assertion here

    def test_create_a_user(self):
        """It should create a User and assert that it exist"""
        data = {
            'uid': '123456789',
            'username': "user1",
            'email': "user@example.com",
            'password': "secret",
            'token': "0123456789",
            'date_joined': "2021-07-27"
        }
        user = User()
        user.dt_name = "user_test"
        user.deserialize(data)
        print("user des ")
        user.create()
        print("user created ")
        self.assertIsNotNone(user.uid)  # add assertion here

    def test_get_a_user(self):
        """It should add a User and get it to assert that it exist"""
        data = {
            'uid': '123456789',
            'username': "user1",
            'email': "user@example.com",
            'password': "secret",
            'token': "0123456789",
            'date_joined': "2021-07-27"
        }
        user = User()
        User.dt_name = "user_test"
        user.deserialize(data)
        # create test user
        user.create()
        # read user data
        read_user = User.find(user.uid)
        self.assertEqual(user.username, read_user.username)  # add assertion here

    def test_update_a_user(self):
        """It should update a User and get it and assert it updated data """
        data = {
            'uid': '123456789',
            'username': "user1",
            'email': "user@example.com",
            'password': "secret",
            'token': "0123456789",
            'date_joined': "2021-07-27"
        }
        user = User()
        User.dt_name = "user_test"
        user.deserialize(data)
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
        data = {
            'uid': '123456789',
            'username': "user1",
            'email': "user@example.com",
            'password': "secret",
            'token': "0123456789",
            'date_joined': "2021-07-27"
        }
        user = User()
        User.dt_name = "user_test"
        user.deserialize(data)
        # create test user
        user.create()
        # read user data
        read_user = User.find(user.uid)
        self.assertEqual(user.username, read_user.username)  # add assertion here
        # user created successfully
        user.delete()
        read_user = User.check_if_exist(user.uid)
        self.assertIsNone(read_user.username)

    def test_get_all_users(self):
        """It should update a User and get it and assert it updated data """
        data = {
            'uid': '123456789',
            'username': "user1",
            'email': "user@example.com",
            'password': "secret",
            'token': "0123456789",
            'date_joined': "2021-07-27"
        }
        user = User()
        User.dt_name = "user_test"
        user.deserialize(data)
        # create test user
        user.create()
        # read user data
        users = User.all()
        self.assertIsNotNone(User)


if __name__ == '__main__':
    unittest.main()
