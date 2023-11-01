import unittest
import logging

from firebase_admin import db
from src.Player.player_model import Player
from tests.factories import PlayerFactory
from src.common import status, errors
from src.Player.player_service import PlayerService
from src.Player.player_validator import validate_player

dt_node = "test"


class TestPlayerModel(unittest.TestCase):
    """ Test Suite for Player Model """

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        # Player.dt_name = dt_node

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.reference(dt_node).delete()
        Player.dt_name = "players"

    def setUp(self):
        """This runs before each test"""
        Player.dt_name = dt_node
        db.reference(dt_node).child("players_table").delete()

    def tearDown(self):
        """This runs after each test"""

        db.reference(dt_node).child("players_table").delete()

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
        des = player.deserialize(ser)
        self.assertEqual(des.name, ser['name'])

    def test_create_player(self):
        """It should create a Player"""
        player = PlayerFactory()
        player.create()
        print(Player.check_if_exist(player.pid))
        self.assertTrue(Player.check_if_exist(player.pid), f"db-player-id: {player.pid}")

    def test_read_player(self):
        """It should find and deserialize a Player"""
        temp_player = PlayerFactory()
        temp_player.create()
        # find and deserialize player
        player = Player.find(temp_player.pid)
        self.assertEqual(player.pid, temp_player.pid)
        self.assertEqual(player.name, temp_player.name)

    def test_update_player(self):
        """It should create a player then update it"""
        player = PlayerFactory()
        player.create()
        name = player.name
        # update player with new name
        player.name = "the kick boxer"
        player.update()
        self.assertNotEquals(player.name, name)
        self.assertEqual(player.name, "the kick boxer")

    def test_delete_player(self):
        """It should delete a player"""
        player = PlayerFactory()
        player.create()
        serial = player.serialize()
        # delete a player
        player.delete()
        self.assertIsNone(Player.find(serial['pid']))
        self.assertFalse(Player.check_if_exist(serial['pid']))

    ######################################################################
    #  T E S T   P L A Y E R   S E R V I C E   M O D E L S
    ######################################################################

    def test_create_usecase(self):
        """It should test create usecase in player service"""
        service = PlayerService()
        fake_player = PlayerFactory()
        validate_player(fake_player.serialize())
        self.assertEqual(service.create_player_usecase(fake_player.serialize()), status.HTTP_201_CREATED)

    def test_read_usecase(self):
        """It should read a player from service"""
        service = PlayerService()
        player = PlayerFactory()
        player.create()
        player2 = service.read_player_usecase(player.pid)
        self.assertEqual(player.name, player2.name)

    def test_update_usecase(self):
        """It should update a player from service"""
        service = PlayerService()
        player = PlayerFactory()
        player.create()
        name = player.name
        # update
        player.name = "Test"
        service.update_player_usecase(player.serialize())
        self.assertEqual(service.read_player_usecase(player.pid).name, player.name)
        self.assertNotEquals(service.read_player_usecase(player.pid), name)

    def test_delete_usecase(self):
        """It should delete a player from service"""
        service = PlayerService()
        player = PlayerFactory()
        player.create()
        pid = player.pid
        # delete
        service.delete_player_usecase(player.pid)
        self.assertFalse(Player.check_if_exist(pid))
        self.assertEqual(service.read_player_usecase(pid), status.HTTP_404_NOT_FOUND)
