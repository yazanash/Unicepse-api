import unittest
from db import db
from src.handshake.handshake_model import HandShake
from tests.factories import HandShakeFactory

sids = []


class TestHandShake(unittest.TestCase):
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
        db.handshakes.delete_many({})

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_range(self, count):
        """Helper method for creating payments in bulk
        """
        handshakes = []
        for _ in range(count):
            handshake = HandShakeFactory()

            handshake.create()
            handshakes.append(handshake)
        return handshakes

    ######################################################################
    #  T E S T   H A N D S H A K E   M O D E L
    ######################################################################

    def test_serialize_hand_shake(self):
        """It should serialize a subscription"""
        handshake = HandShakeFactory()
        serialized = handshake.serialize()

        self.assertEqual(serialized['gym_id'], handshake.gym_id)
        self.assertEqual(serialized['pid'], handshake.pid)
        self.assertEqual(serialized['uid'], handshake.uid)

    def test_deserialize_hand_shake(self):
        """It should deserialize a payment"""
        handshake = HandShakeFactory()
        deserialized = HandShake.create_model()
        deserialized.deserialize(handshake.serialize())
        print(deserialized.serialize())
        self.assertEqual(deserialized.pid, handshake.pid)
        self.assertEqual(deserialized.uid, handshake.uid)
        self.assertEqual(deserialized.gym_id, handshake.gym_id)

    def test_create_hand_shake(self):
        """It should create subscription with no payments"""
        handshake = HandShakeFactory()
        handshake.create()
        temp_pay = HandShake.find(handshake.gym_id, handshake.pid, handshake.uid)
        self.assertEqual(temp_pay.pid, handshake.pid)

    def test_read_all_hand_shakes(self):
        """It should read all subscriptions"""
        handshakes_list = self._create_range(5)
        print(handshakes_list)
        pid = handshakes_list[0].pid
        uid = handshakes_list[0].uid
        gym_id = handshakes_list[0].gym_id
        temp_list = HandShake.all(gym_id, pid, uid)
        for i in range(4):
            print(i)
            print(temp_list[i].serialize())
            self.assertEqual(temp_list[i].serialize(), handshakes_list[i].serialize())


