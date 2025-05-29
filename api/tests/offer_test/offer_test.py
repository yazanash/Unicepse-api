import unittest
from db import db
from src.offer.offer_model import Offer
from api.tests.factories import OfferFactory

sids = []


class TestOffer(unittest.TestCase):
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
        db.offers.delete_many({})

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################
    def _create_range(self, count):
        """Helper method for creating payments in bulk
        """
        offers = []
        for _ in range(count):
            offer = OfferFactory()
            offer.create()
            offers.append(offer)
        return offers

    ######################################################################
    #  T E S T   P L A N   M O D E L
    ######################################################################

    def test_serialize_offer(self):
        """It should serialize am offer"""
        offer = OfferFactory()
        serialized = offer.serialize()

        self.assertEqual(serialized['offer_name'], offer.offer_name)
        self.assertEqual(serialized['description'], offer.description)
        self.assertEqual(serialized['offer_percent'], offer.offer_percent)

    def test_deserialize_offer(self):
        """It should deserialize an offer"""
        offer = OfferFactory()
        deserialized = offer.create_model()
        deserialized.deserialize(offer.serialize())
        self.assertEqual(deserialized.offer_name, offer.offer_name)
        self.assertEqual(deserialized.offer_percent, offer.offer_percent)
        self.assertEqual(deserialized.description, offer.description)

    def test_create_offer(self):
        """It should create offer"""
        offer = OfferFactory()
        offer.create()
        temp_offer = Offer.find(offer.id)
        self.assertEqual(temp_offer.offer_name, offer.offer_name)

    def test_update_offer(self):
        """It should create offer"""
        offer = OfferFactory()
        offer.create()
        temp_offer_name = "my offer"
        offer.offer_name = temp_offer_name
        offer.update()
        temp_offer = Offer.find(offer.id)
        self.assertEqual(temp_offer.offer_name, temp_offer_name)

    def test_read_offer(self):
        """It should read an offer"""
        offer = OfferFactory()
        offer.create()
        temp_offer = Offer.find(offer.id)
        self.assertEqual(temp_offer.offer_name, offer.offer_name)
        self.assertEqual(temp_offer.offer_percent, offer.offer_percent)
        self.assertEqual(temp_offer.period, offer.period)

    def test_read_offers(self):
        """It should read all offer"""
        offers_list = self._create_range(5)
        temp_list = Offer.all()
        for i in range(4):
            self.assertEqual(temp_list[i].serialize(), offers_list[i].serialize())


