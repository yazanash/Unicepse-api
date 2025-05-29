import unittest
from api.tests.factories import PlayerFactory
from src.Player.player_model import Player
from src.common import status
from app import app
from db import db


PLAYER_URL = "/player"
dt_node = "players"
test_gym_id = 18

json_type = "application/json"


class TestPlayerRoutes(unittest.TestCase):
    """Test Suite for player route"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""

    def setUp(self):
        """This runs before each test"""
        self.client = app.test_client()

    def tearDown(self):
        """This runs after each test"""
        players_node = db.players
        players_node.drop()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_players(self, count):
        """Factory method to create accounts in bulk"""
        accounts = []
        for _ in range(count):
            account = PlayerFactory()
            account.gym_id = test_gym_id
            response = self.client.post(PLAYER_URL, json=account.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Account",
            )
            accounts.append(account)
        return accounts

    ######################################################################
    #  T E S T   P L A Y E R   R O U T E S
    ######################################################################
    def test_create_player_route(self):
        """It should CREATE player through route service"""
        player = PlayerFactory()
        player.gym_id = test_gym_id
        resp = self.client.post(
            PLAYER_URL,
            json=player.serialize(),
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_bad_request(self):
        """It should check for valid data on create route"""
        resp = self.client.post(PLAYER_URL, json={'name': "not enough data"}, content_type=json_type)
        self.assertEqual(resp.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_read_player_route(self):
        """It should READ player through route service"""
        players_list = self._create_players(3)
        resp1 = self.client.get(f"{PLAYER_URL}/{players_list[0].gym_id}/{players_list[0].pid}")
        self.assertEqual(resp1.get_json()["pid"], players_list[0].pid)

        resp2 = self.client.get(f"{PLAYER_URL}/{players_list[1].gym_id}/{players_list[1].pid}")
        self.assertEqual(resp2.get_json(), players_list[1].serialize())

        resp3 = self.client.get(f"{PLAYER_URL}/{players_list[2].gym_id}/{players_list[2].pid}")
        self.assertEqual(resp3.get_json(), players_list[2].serialize())

    def test_read_bad_request(self):
        """It should check for valid id on READ player"""
        resp = self.client.get(f"{PLAYER_URL}/18")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_player_route(self):
        """It should UPDATE player through route service"""
        players_list = self._create_players(1)
        player = players_list[0]
        name = player.name
        player.name = "testimonial"
        resp = self.client.put(
            PLAYER_URL,
            json=player.serialize(),
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        response = self.client.get(f"{PLAYER_URL}/{player.gym_id}/{player.pid}")
        temp = Player.create_model()
        temp.deserialize(response.get_json())
        self.assertEqual(temp.name, player.name)
        self.assertNotEqual(temp.name, name)

    def test_update_bad_request(self):
        """It should check for valid data in update player"""
        self._create_players(1)
        resp = self.client.put(
            PLAYER_URL,
            json={'name': 'not enough data'},
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_406_NOT_ACCEPTABLE)
