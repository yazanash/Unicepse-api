import unittest

from src.offer.offer_model import Offer
from tests.factories import OfferFactory
from src.common import status
from app import app
from db import db


OFFERS_URL = "/api/v1/offers"
dt_node = "offers"

json_type = "application/json"


class TestOfferRoutes(unittest.TestCase):
    """Test Suite for offer route"""

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
        db.offers.delete_many({})

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_offer(self, count):
        """Factory method to create accounts in bulk"""
        offers = []
        for _ in range(count):
            offer = OfferFactory()
            response = self.client.post(OFFERS_URL, json=offer.serialize_to_data_base())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Account",
            )
            offer.id = response.get_json()["message"]
            offers.append(offer)
        return offers

    ######################################################################
    #  T E S T   O F F E R   R O U T E S
    ######################################################################
    def test_create_offer_route(self):
        """It should CREATE offer through route service"""
        offer = OfferFactory()
        resp = self.client.post(
            OFFERS_URL,
            json=offer.serialize_to_data_base(),
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_bad_request(self):
        """It should check for valid data on create route"""
        resp = self.client.post(OFFERS_URL, json={'offer': "not enough data"}, content_type=json_type)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_read_offers_route(self):
        """It should READ all offer through route service"""
        offers_list = self._create_offer(5)
        resp1 = self.client.get(f"{OFFERS_URL}")
        for i in range(4):
            self.assertEqual(offers_list[i].serialize(), resp1.get_json()[i])

    def test_read_offer_route(self):
        """It should READ offer through route service"""
        offers_list = self._create_offer(3)
        resp1 = self.client.get(f"{OFFERS_URL}/{offers_list[0].id}")
        self.assertEqual(resp1.get_json()["offer_name"], offers_list[0].offer_name)

        resp2 = self.client.get(f"{OFFERS_URL}/{offers_list[1].id}")
        self.assertEqual(resp2.get_json(), offers_list[1].serialize())

        resp3 = self.client.get(f"{OFFERS_URL}/{offers_list[2].id}")
        self.assertEqual(resp3.get_json(), offers_list[2].serialize())

    def test_read_bad_request(self):
        """It should check for valid id on READ offer"""
        resp = self.client.get(f"{OFFERS_URL}/1599999")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_offer_route(self):
        """It should UPDATE offer through route service"""
        offers_list = self._create_offer(1)
        offer = offers_list[0]
        name = offer.offer_name
        offer.offer_name = "testimonial"
        resp = self.client.put(
            f"{OFFERS_URL}/{offer.id}",
            json=offer.serialize_to_data_base(),
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        response = self.client.get(f"{OFFERS_URL}/{offer.id}")
        temp = Offer.create_model()
        temp.deserialize(response.get_json())
        self.assertEqual(temp.offer_name, offer.offer_name)
        self.assertNotEqual(temp.offer_name, name)

    def test_update_bad_request(self):
        """It should check for valid data in update offer"""
        offer_list = self._create_offer(1)
        offer = offer_list[0]
        resp = self.client.put(
            f"{OFFERS_URL}/{offer.id}",
            json={'plan_name': 'not enough data'},
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_406_NOT_ACCEPTABLE)
