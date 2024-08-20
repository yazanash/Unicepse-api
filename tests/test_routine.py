import json
import unittest
from db import db
from src.routine.routine_model import Routine

test_gym_id = 18
dt_node = "routines"


class TestRoutineModel(unittest.TestCase):
    """ test suit for routine model"""
    def tearDown(self):
        """this runs after each test"""
        routine_path = db["Gyms"][test_gym_id][dt_node]
        routine_path.delete_many({})

    ######################################################################
    #  T E S T   P L A Y E R   M O D E L S
    ######################################################################

    def test_serialize_routine(self):
        """It should serialize a routine with no errors"""
        with open('player_routine.json', 'r') as json_file:
            routine = json.load(json_file)
            routine_ob = Routine.create_model()
            routine_ob.deserialize(routine)
            ser = routine_ob.serialize()
            self.assertEqual(ser['RoutineId'], routine_ob.lid)

    def test_deserialize_routine(self):
        """It should deserialize a routine with no errors"""
        with open('player_routine.json', 'r') as json_file:
            routine = json.load(json_file)
            routine_ob = Routine.create_model()
            routine_ob.deserialize(routine)
            routine_ob.gym_id = test_gym_id
            self.assertEqual(routine_ob.lid, routine['RoutineId'])

    def test_create_routine(self):
        """It should deserialize a routine with no errors"""
        with open('player_routine.json', 'r') as json_file:
            routine = json.load(json_file)
            routine_ob = Routine.create_model()
            routine_ob.deserialize(routine)
            routine_ob.gym_id = test_gym_id
            routine_ob.create()
            self.assertTrue(Routine.check_if_exist(test_gym_id, routine_ob.lid), f"db-routine-id: {routine_ob.lid}")

    def test_read_routine(self):
        """It should find and deserialize a Player"""
        with open('player_routine.json', 'r') as json_file:
            routine = json.load(json_file)
            routine_ob = Routine.create_model()
            routine_ob.deserialize(routine)
            routine_ob.gym_id = test_gym_id
            routine_ob.create()
            # find and deserialize player
            new_routine = Routine.find(test_gym_id, routine_ob.lid)

            self.assertEqual(new_routine.lid, routine_ob.lid)
            self.assertEqual(new_routine.routine_no, routine_ob.routine_no)

    def test_update_routine(self):
        """It should find and deserialize a Player"""
        with open('player_routine.json', 'r') as json_file:
            routine = json.load(json_file)
            routine_ob = Routine.create_model()
            routine_ob.deserialize(routine)
            routine_ob.gym_id = test_gym_id
            routine_ob.create()
            # find and deserialize player
            old_num = routine_ob.routine_no
            routine_ob.routine_no = 100
            routine_ob.update()
            self.assertNotEquals(routine_ob.routine_no, old_num)
            self.assertEqual(routine_ob.routine_no, 100)
