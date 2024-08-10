import unittest
from db import db
from src.gym.gym_model import Gym
from src.plans.plan_model import Plan
from tests.factories import GymFactory, PlanFactory

sids = []


class TestPlan(unittest.TestCase):
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
        db.plans.delete_many({})

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################
    def _create_range(self, count):
        """Helper method for creating payments in bulk
        """
        plans = []
        for _ in range(count):
            plan = PlanFactory()
            plan.create()
            plans.append(plan)
        return plans

    ######################################################################
    #  T E S T   P L A N   M O D E L
    ######################################################################

    def test_serialize_plan(self):
        """It should serialize a plan"""
        plan = PlanFactory()
        serialized = plan.serialize()

        self.assertEqual(serialized['plan_name'], plan.plan_name)
        self.assertEqual(serialized['description'], plan.description)
        self.assertEqual(serialized['price'], plan.price)

    def test_deserialize_plan(self):
        """It should deserialize a plan"""
        plan = PlanFactory()
        deserialized = plan.create_model()
        deserialized.deserialize(plan.serialize())
        self.assertEqual(deserialized.plan_name, plan.plan_name)
        self.assertEqual(deserialized.price, plan.price)
        self.assertEqual(deserialized.description, plan.description)

    def test_create_plan(self):
        """It should create plan"""
        plan = PlanFactory()
        plan.create()
        temp_plan = Plan.find(plan.id)
        self.assertEqual(temp_plan.plan_name, plan.plan_name)

    def test_update_gym(self):
        """It should create plan"""
        plan = PlanFactory()
        plan.create()
        temp_plan_name = "my gym"
        plan.plan_name = temp_plan_name
        plan.update()
        temp_plan = Plan.find(plan.id)
        self.assertEqual(temp_plan.plan_name, temp_plan_name)

    def test_read_plan(self):
        """It should read a plan"""
        plan = PlanFactory()
        plan.create()
        temp_plan = Plan.find(plan.id)
        self.assertEqual(temp_plan.plan_name, plan.plan_name)
        self.assertEqual(temp_plan.price, plan.price)
        self.assertEqual(temp_plan.period, plan.period)

    def test_read_plans(self):
        """It should read all plan"""
        plans_list = self._create_range(5)
        temp_list = Plan.all()
        for i in range(4):
            self.assertEqual(temp_list[i].serialize(), plans_list[i].serialize())


