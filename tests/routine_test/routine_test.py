import unittest
from db import db
from src.routine.routine_model import Routine
from tests.factories import RoutineFactory

sids = []


class TestRoutine(unittest.TestCase):
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
        db.routines.delete_many({})

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################
    def _create_range(self, count):
        """Helper method for creating payments in bulk
        """
        routines = []
        for _ in range(count):
            routine = RoutineFactory()

            routine.create()
            routines.append(routine)
        return routines

    ######################################################################
    #  T E S T   R O U T I N E   M O D E L
    ######################################################################

    def test_serialize_routine(self):
        """It should serialize a routine"""
        routine = RoutineFactory()
        serialized = routine.serialize()

        self.assertEqual(serialized['routine_no'], routine.routine_no)
        self.assertEqual(serialized['routine_date'], routine.routine_date)
        self.assertEqual(serialized['rid'], routine.rid)

    def test_deserialize_routine(self):
        """It should deserialize a routine"""
        routine = RoutineFactory()
        deserialized = Routine.create_model()
        deserialized.deserialize(routine.serialize())
        self.assertEqual(deserialized.routine_no, routine.routine_no)
        self.assertEqual(deserialized.routine_date, routine.routine_date)
        self.assertEqual(deserialized.rid, routine.rid)

    def test_create_routine(self):
        """It should create routine"""
        routine = RoutineFactory()
        routine.create()
        temp_routine = Routine.find_by_rid(routine.gym_id, routine.pid, routine.rid)
        self.assertEqual(temp_routine.routine_no, routine.routine_no)

    def test_update_routine(self):
        """It should create routine"""
        routine = RoutineFactory()
        routine.create()
        temp_routine_no = "my gym"
        routine.routine_no = temp_routine_no
        routine.update()
        temp_routine = Routine.find_by_rid(routine.gym_id, routine.pid, routine.rid)
        self.assertEqual(temp_routine.routine_no, temp_routine_no)

    def test_read_routine(self):
        """It should read all subscriptions"""
        routine = RoutineFactory()
        routine.create()
        temp_routine = Routine.find_by_rid(routine.gym_id, routine.pid, routine.rid)
        self.assertEqual(temp_routine.routine_no, routine.routine_no)
        self.assertEqual(temp_routine.routine_date, routine.routine_date)
        self.assertEqual(temp_routine.rid, routine.rid)
