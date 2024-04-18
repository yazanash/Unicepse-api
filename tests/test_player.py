import unittest

from db import db
from src.Player.player_model import Player
from tests.factories import PlayerFactory
from src.common import status
from src.Player.player_service import PlayerService
from src.Player.player_validator import validate_player

dt_node = "players"
test_gym_id = 18


class TestPlayerModel(unittest.TestCase):
    """ Test Suite for Player Model """

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
        players_node = db["Gyms"][test_gym_id][dt_node]
        print(players_node)
        players_node.drop()

    ######################################################################
    #  T E S T   P L A Y E R   M O D E L S
    ######################################################################

    def test_serialize_player(self):
        """It should serialize a player with no errors"""
        player = PlayerFactory()
        ser = player.serialize()
        self.assertEqual(ser['name'], player.name)

    def test_deserialize_player(self):
        """It should deserialize a player with no errors"""
        player = PlayerFactory()
        ser = player.serialize()
        player.deserialize(ser)
        self.assertEqual(player.name, ser['name'])

    def test_create_player(self):
        """It should create a Player"""
        player = PlayerFactory()
        player.gym_id = test_gym_id
        player.create()
        self.assertTrue(Player.check_if_exist(test_gym_id, player.pid), f"db-player-id: {player.pid}")

    def test_read_player(self):
        """It should find and deserialize a Player"""
        temp_player = PlayerFactory()
        temp_player.gym_id = test_gym_id
        temp_player.create()
        # find and deserialize player
        player = Player.find(test_gym_id, temp_player.pid)

        self.assertEqual(player.pid, temp_player.pid)
        self.assertEqual(player.name, temp_player.name)

    def test_update_player(self):
        """It should create a player then update it"""
        player = PlayerFactory()
        player.gym_id = test_gym_id
        player.create()
        name = player.name
        # update player with new name
        player.name = "the kick boxer"
        player.update()
        self.assertNotEquals(player.name, name)
        self.assertEqual(player.name, "the kick boxer")

    ######################################################################
    #  T E S T   P L A Y E R   S E R V I C E   M O D E L S
    ######################################################################

    def test_create_use_case(self):
        """It should test create use_case in player service"""
        service = PlayerService()
        fake_player = PlayerFactory()
        fake_player.gym_id = test_gym_id
        validate_player(fake_player.serialize())
        self.assertEqual(service.create_player_usecase(fake_player.serialize()), status.HTTP_201_CREATED)

    def test_read_use_case(self):
        """It should read a player from service"""
        service = PlayerService()
        player = PlayerFactory()
        player.gym_id = test_gym_id
        player.create()
        player2 = service.read_player_usecase(test_gym_id, player.pid)
        self.assertEqual(player.name, player2.name)

    def test_update_use_case(self):
        """It should update a player from service"""
        service = PlayerService()
        player = PlayerFactory()
        player.gym_id = test_gym_id
        player.create()
        name = player.name
        # update
        player.name = "Test"
        service.update_player_usecase(player.serialize())
        self.assertEqual(service.read_player_usecase(test_gym_id, player.pid).name, player.name)
        self.assertNotEquals(service.read_player_usecase(test_gym_id, player.pid), name)

