import unittest
import logging

from firebase_admin import db
from src.Player.player_presistent_base import PlayerPersistentBase
from src.Player.player_model import Player
from tests.factories import PlayerFactory
from src.common import status

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

    def test_create_player_with_error(self):
        """It should raise Exception on invalid create"""
        player = Player()

        # with Empty
        self.assertRaises(AttributeError, player.create)

        # with pid
        player.pid = 0
        self.assertRaises(AttributeError, player.create)
        player.pid = None

        # with date
        player.date_of_birth = "2000/01/15 01:01:01"
        self.assertRaises(AttributeError, player.create)
        player.date_of_birth = None

