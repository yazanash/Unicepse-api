import unittest

from dotenv import load_dotenv

from db import db
from src.license.license_model import License
from tests.factories import LicenseFactory

sids = []


class TestLicense(unittest.TestCase):
    """ Test Suite for Subscription Model """

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        load_dotenv()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""

    def setUp(self):
        """This runs before each test"""
        load_dotenv()

    def tearDown(self):
        """This runs after each test"""
        db.licenses.delete_many({})

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_range(self, count):
        """Helper method for creating licenses in bulk
        """
        licenses = []
        for _ in range(count):
            gym_license = LicenseFactory()
            gym_license.create()
            licenses.append(gym_license)
        return licenses

    ######################################################################
    #  T E S T   H A N D S H A K E   M O D E L
    ######################################################################

    def test_serialize_license(self):
        """It should serialize a license"""
        gym_license = LicenseFactory()
        serialized = gym_license.serialize_secret()

        self.assertEqual(serialized['gym_id'], gym_license.gym_id)
        self.assertEqual(serialized['plan_id'], gym_license.plan_id)
        self.assertEqual(serialized['price'], gym_license.price)

    def test_deserialize_license(self):
        """It should deserialize a license"""
        gym_license = LicenseFactory()
        deserialized = License.create_model()
        deserialized.deserialize_secret(gym_license.serialize_secret())
        self.assertEqual(deserialized.plan_id, gym_license.plan_id)
        self.assertEqual(deserialized.price, gym_license.price)
        self.assertEqual(deserialized.gym_id, gym_license.gym_id)

    def test_create_license(self):
        """It should create license"""
        gym_license = LicenseFactory()
        gym_license.create()
        temp_pay = License.find(gym_license.gym_id, gym_license.plan_id)
        self.assertEqual(temp_pay.plan_id, gym_license.plan_id)

    def test_update_license(self):
        """It should update license"""
        gym_license = LicenseFactory()
        gym_license.create()
        price = 15000.00
        gym_license.price = price
        gym_license.update()
        temp_pay = License.find(gym_license.gym_id, gym_license.plan_id)
        self.assertEqual(temp_pay.price, price)

    def test_read_all_licenses(self):
        """It should read all licenses"""
        licenses_list = self._create_range(5)
        print(licenses_list)
        temp_list = License.all()
        for i in range(4):
            print(licenses_list[i].serialize())
            print(temp_list[i].serialize())
            self.assertEqual(temp_list[i].serialize(), licenses_list[i].serialize())

    def test_read_all_gym_licenses(self):
        """It should read all licenses"""
        licenses_list = self._create_range(5)
        gym_id = licenses_list[0].gym_id
        temp_list = License.all_license(gym_id)
        for i in range(4):
            self.assertEqual(temp_list[i].serialize(), licenses_list[i].serialize())
