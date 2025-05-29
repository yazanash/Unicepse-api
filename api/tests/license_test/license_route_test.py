import unittest

from dotenv import load_dotenv

from src.license.license_model import License
from api.tests.factories import LicenseFactory
from src.common import status
from app import app
from db import db


LICENSES_URL = "/api/v1/licenses"
dt_node = "licenses"
test_gym_id = 18

json_type = "application/json"


class TestLicenseRoutes(unittest.TestCase):
    """Test Suite for subscription route"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        load_dotenv()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""

    def setUp(self):
        """This runs before each test"""
        self.client = app.test_client()
        load_dotenv()

    def tearDown(self):
        """This runs after each test"""
        db.licenses.delete_many({})

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_license(self, count):
        """Factory method to create accounts in bulk"""
        licenses = []
        for _ in range(count):
            gym_license = LicenseFactory()
            response = self.client.post(LICENSES_URL, json=gym_license.serialize_secret())
            resp = response.get_json()
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Account",
            )
            # gym_license._id = resp["lid"]
            new_gym_license = License.create_model()
            print(type(resp['data']))
            new_gym_license.deserialize_from_data_base(resp["data"])
            licenses.append(new_gym_license)
        return licenses

    ######################################################################
    #  T E S T   L I C E N S E   R O U T E S
    ######################################################################
    def test_create_license_route(self):
        """It should CREATE license through route service"""
        gym_license = LicenseFactory()
        resp = self.client.post(
            LICENSES_URL,
            json=gym_license.serialize_secret(),
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_update_license_route(self):
        """It should UPDATE license through route service"""
        licenses_list = self._create_license(1)
        gym_license = licenses_list[0]
        gym_license.price = 150000.00
        print(gym_license.serialize_secret())
        resp = self.client.put(
            f"{LICENSES_URL}/{gym_license._id}",
            json=gym_license.serialize_secret(),
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        response = self.client.get(f"{LICENSES_URL}/{gym_license._id}")
        print(response.get_json())
        temp = License.create_model()
        temp.deserialize(response.get_json())
        self.assertEqual(temp.price, gym_license.price)

    def test_bad_request(self):
        """It should check for valid data on create route"""
        resp = self.client.post(LICENSES_URL, json={'plan': "not enough data"}, content_type=json_type)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_read_licenses_route(self):
        """It should READ license through route service"""
        licenses_list = self._create_license(5)
        resp1 = self.client.get(f"{LICENSES_URL}")

        for i in range(4):
            self.assertEqual(licenses_list[i].serialize(), resp1.get_json()[i])

    def test_read_gym_license_route(self):
        """It should READ license through route service"""
        licenses_list = self._create_license(5)
        print(f"call started for gym{licenses_list[0].gym_id}")
        resp1 = self.client.get(f"{LICENSES_URL}/gym/18")
        print(f"call started for gym{licenses_list[0].gym_id}")

        for i in range(4):
            self.assertEqual(licenses_list[i].serialize(), resp1.get_json()[i])

