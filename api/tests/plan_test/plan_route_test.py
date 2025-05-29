import unittest

from src.plans.plan_model import Plan
from api.tests.factories import PlanFactory
from src.common import status
from app import app
from db import db


PLANS_URL = "/api/v1/plans"
dt_node = "plans"

json_type = "application/json"


class TestPlanRoutes(unittest.TestCase):
    """Test Suite for plan route"""

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
        db.plans.delete_many({})

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_plan(self, count):
        """Factory method to create accounts in bulk"""
        plans = []
        for _ in range(count):
            plan = PlanFactory()
            response = self.client.post(PLANS_URL, json=plan.serialize_to_data_base())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Account",
            )
            plan.id = response.get_json()["message"]
            plans.append(plan)
        return plans

    ######################################################################
    #  T E S T   P L A N   R O U T E S
    ######################################################################
    def test_create_plan_route(self):
        """It should CREATE plan through route service"""
        plan = PlanFactory()
        resp = self.client.post(
            PLANS_URL,
            json=plan.serialize_to_data_base(),
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_bad_request(self):
        """It should check for valid data on create route"""
        resp = self.client.post(PLANS_URL, json={'plan': "not enough data"}, content_type=json_type)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_read_plans_route(self):
        """It should READ all gyms through route service"""
        plans_list = self._create_plan(5)
        resp1 = self.client.get(f"{PLANS_URL}")
        for i in range(4):
            self.assertEqual(plans_list[i].serialize(), resp1.get_json()[i])

    def test_read_plan_route(self):
        """It should READ gym through route service"""
        plans_list = self._create_plan(3)
        resp1 = self.client.get(f"{PLANS_URL}/{plans_list[0].id}")
        self.assertEqual(resp1.get_json()["plan_name"], plans_list[0].plan_name)

        resp2 = self.client.get(f"{PLANS_URL}/{plans_list[1].id}")
        self.assertEqual(resp2.get_json(), plans_list[1].serialize())

        resp3 = self.client.get(f"{PLANS_URL}/{plans_list[2].id}")
        self.assertEqual(resp3.get_json(), plans_list[2].serialize())

    def test_read_bad_request(self):
        """It should check for valid id on READ plan"""
        resp = self.client.get(f"{PLANS_URL}/1599999")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_plan_route(self):
        """It should UPDATE plan through route service"""
        plans_list = self._create_plan(1)
        plan = plans_list[0]
        name = plan.plan_name
        plan.plan_name = "testimonial"
        resp = self.client.put(
            f"{PLANS_URL}/{plan.id}",
            json=plan.serialize_to_data_base(),
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        response = self.client.get(f"{PLANS_URL}/{plan.id}")
        temp = Plan.create_model()
        temp.deserialize(response.get_json())
        self.assertEqual(temp.plan_name, plan.plan_name)
        self.assertNotEqual(temp.plan_name, name)

    def test_update_bad_request(self):
        """It should check for valid data in update player"""
        plan_list = self._create_plan(1)
        plan = plan_list[0]
        resp = self.client.put(
            f"{PLANS_URL}/{plan.id}",
            json={'plan_name': 'not enough data'},
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_406_NOT_ACCEPTABLE)
