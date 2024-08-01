import unittest
from db import db
from src.gym.gym_model import Gym
from tests.factories import HandShakeFactory, GymFactory

sids = []


class TestGym(unittest.TestCase):
    """ Test Suite for Subscription Model """

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""

    def setUp(self):
        """This runs before each test"""

    def tearDown(self):
        """This runs after each test"""
        db.gyms.delete_many({})

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################
    def _create_range(self, count):
        """Helper method for creating payments in bulk
        """
        gyms = []
        for _ in range(count):
            gym = GymFactory()

            gym.create()
            gyms.append(gym)
        return gyms

    ######################################################################
    #  T E S T   G Y M   M O D E L
    ######################################################################

    def test_serialize_gym(self):
        """It should serialize a gym"""
        gym = GymFactory()
        serialized = gym.serialize()

        self.assertEqual(serialized['gym_name'], gym.gym_name)
        self.assertEqual(serialized['phone_number'], gym.phone_number)
        self.assertEqual(serialized['owner_name'], gym.owner_name)

    def test_deserialize_gym(self):
        """It should deserialize a gym"""
        gym = GymFactory()
        deserialized = gym.create_model()
        deserialized.deserialize(gym.serialize())
        self.assertEqual(deserialized.gym_name, gym.gym_name)
        self.assertEqual(deserialized.phone_number, gym.phone_number)
        self.assertEqual(deserialized.owner_name, gym.owner_name)

    def test_create_gym(self):
        """It should create gym"""
        gym = GymFactory()
        gym.create()
        temp_gym = Gym.find(gym.id)
        self.assertEqual(temp_gym.gym_name, gym.gym_name)

    def test_update_gym(self):
        """It should create gym"""
        gym = GymFactory()
        gym.create()
        temp_gym_name = "my gym"
        gym.gym_name = temp_gym_name
        gym.update()
        temp_gym = Gym.find(gym.id)
        self.assertEqual(temp_gym.gym_name, temp_gym_name)

    def test_read_gym(self):
        """It should read all subscriptions"""
        gym = GymFactory()
        gym.create()
        temp_gym = Gym.find(gym.id)
        self.assertEqual(temp_gym.gym_name, gym.gym_name)
        self.assertEqual(temp_gym.phone_number, gym.phone_number)
        self.assertEqual(temp_gym.owner_name, gym.owner_name)

    def test_read_gyms(self):
        """It should read all subscriptions"""
        gyms_list = self._create_range(5)
        temp_list = Gym.all()
        for i in range(4):
            self.assertEqual(temp_list[i].serialize(), gyms_list[i].serialize())


