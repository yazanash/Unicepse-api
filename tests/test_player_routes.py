import unittest
from .factories import PlayerFactory
from src.Player.player_model import Player
from src.Player.player_service import PlayerService
from src.common import status
from src import app
from firebase_admin import db


PLAYER_URL = "/player"
dt_node = "test"

json_type = "application/json"


class TestPlayerRoutes(unittest.TestCase):
    """Test Suite for player route"""

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

        self.client = app.test_client()

    def tearDown(self):
        """This runs after each test"""
        db.reference(dt_node).child("players_table").delete()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_players(self, count):
        """Factory method to create accounts in bulk"""
        accounts = []
        for _ in range(count):
            account = PlayerFactory()
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

        resp1 = self.client.get(PLAYER_URL, json={0: players_list[0].pid}, content_type=json_type)
        print("json from read player: ", resp1.get_json())
        self.assertEqual(resp1.get_json()["pid"], players_list[0].pid)

        resp2 = self.client.get(PLAYER_URL, json={0: players_list[1].pid})
        self.assertEqual(resp2.get_json(), players_list[1].serialize())

        resp3 = self.client.get(PLAYER_URL, json={0: players_list[2].pid}, content_type=json_type)
        self.assertEqual(resp3.get_json(), players_list[2].serialize())

    def test_read_bad_request(self):
        """It should check for valid id on READ player"""
        resp = self.client.get(PLAYER_URL, json={0: 5000})
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
        response = self.client.get(PLAYER_URL, json={0: player.pid})
        temp = Player.deserialize(response.get_json())
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

    def test_delete_player_route(self):
        """It should DELETE player through route service"""
        pid = self._create_players(1)[0].pid
        resp = self.client.delete(PLAYER_URL, json={0: pid})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        res = self.client.get(PLAYER_URL, json={0: pid})
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
