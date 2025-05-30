import unittest

from dotenv import load_dotenv

from db import db
from src.Authentication.profile_model import Profile
from tests.factories import ProfileFactory

dt_node = "profiles"
test_uid = "667f284457207891c7afb3cf"


class TestProfileModel(unittest.TestCase):
    """ Test Suite for Profile Model """

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        load_dotenv()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""

    def setUp(self):
        """This runs before each test"""

    def tearDown(self):
        """This runs after each test"""
        db.profiles.delete_many({})

    ######################################################################
    #  T E S T   P L A Y E R   M O D E L S
    ######################################################################

    def test_serialize_player(self):
        """It should serialize a profile with no errors"""
        profile = ProfileFactory()
        profile.uid = test_uid
        ser = profile.serialize()
        self.assertEqual(ser['full_name'], profile.full_name)

    def test_deserialize_player(self):
        """It should deserialize a profile with no errors"""
        profile = ProfileFactory()
        profile.uid = test_uid
        ser = profile.serialize()
        profile.deserialize(ser)
        self.assertEqual(profile.full_name, ser['full_name'])

    def test_create_profile(self):
        """It should create a Player"""
        profile = ProfileFactory()
        profile.uid = test_uid
        profile.create()
        self.assertTrue(Profile.check_if_exist(test_uid), f"db-player-id: {profile.uid}")

    def test_read_profile(self):
        """It should find and deserialize a Player"""
        temp_profile = ProfileFactory()
        temp_profile.uid = test_uid
        temp_profile.create()
        # find and deserialize player
        profile = Profile.find(test_uid)

        self.assertEqual(profile.uid, temp_profile.uid)
        self.assertEqual(profile.full_name, temp_profile.full_name)

    def test_update_profile(self):
        """It should create a player then update it"""
        profile = ProfileFactory()
        profile.uid = test_uid
        profile.create()
        full_name = profile.full_name
        # update player with new name
        profile.full_name = "the kick boxer"
        profile.update()
        self.assertNotEqual(profile.full_name, full_name)
        self.assertEqual(profile.full_name, "the kick boxer")

    # ######################################################################
    # #  T E S T   P L A Y E R   S E R V I C E   M O D E L S
    # ######################################################################
    #
    # def test_create_use_case(self):
    #     """It should test create use_case in player service"""
    #     service = PlayerService()
    #     fake_player = PlayerFactory()
    #     fake_player.gym_id = test_gym_id
    #     validate_player(fake_player.serialize())
    #     self.assertEqual(service.create_player_usecase(fake_player.serialize()), status.HTTP_201_CREATED)
    #
    # def test_read_use_case(self):
    #     """It should read a player from service"""
    #     service = PlayerService()
    #     player = PlayerFactory()
    #     player.gym_id = test_gym_id
    #     player.create()
    #     player2 = service.read_player_usecase(test_gym_id, player.pid)
    #     self.assertEqual(player.name, player2.name)
    #
    # def test_update_use_case(self):
    #     """It should update a player from service"""
    #     service = PlayerService()
    #     player = PlayerFactory()
    #     player.gym_id = test_gym_id
    #     player.create()
    #     name = player.name
    #     # update
    #     player.name = "Test"
    #     service.update_player_usecase(player.serialize())
    #     self.assertEqual(service.read_player_usecase(test_gym_id, player.pid).name, player.name)
    #     self.assertNotEquals(service.read_player_usecase(test_gym_id, player.pid), name)
    #
