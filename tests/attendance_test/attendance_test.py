import datetime
import unittest
from db import db
from src.attedence.attendance_model import Attendance
from tests.factories import AttendanceFactory


class TestAttendance(unittest.TestCase):
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
        db.attendances.delete_many({})

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################
    def _create_range(self, count):
        """Helper method for creating payments in bulk
        """
        attendances = []
        for _ in range(count):
            attendance = AttendanceFactory()

            attendance.create()
            attendances.append(attendance)
        return attendances

    ######################################################################
    #  T E S T   A T T E N D A N C E   M O D E L
    ######################################################################

    def test_serialize_attendance(self):
        """It should serialize an attendance"""
        attendance = AttendanceFactory()
        serialized = attendance.serialize()

        self.assertEqual(serialized['aid'], attendance.aid)
        self.assertEqual(serialized['date'], attendance.date)
        self.assertEqual(serialized['login_time'], attendance.login_time)
        self.assertEqual(serialized['logout_time'], attendance.logout_time)

    def test_deserialize_attendance(self):
        """It should deserialize an attendance"""
        attendance = AttendanceFactory()
        deserialized = Attendance.create_model()
        deserialized.deserialize(attendance.serialize())
        self.assertEqual(deserialized.aid, attendance.aid)
        self.assertEqual(deserialized.date, attendance.date)
        self.assertEqual(deserialized.logout_time, attendance.logout_time)
        self.assertEqual(deserialized.login_time, attendance.login_time)

    def test_create_attendance(self):
        """It should create gym"""
        attendance = AttendanceFactory()
        attendance.create()
        temp_attendance = Attendance.find(attendance.aid, attendance.gym_id)
        self.assertEqual(temp_attendance.gym_name, attendance.gym_name)

    def test_update_attendance(self):
        """It should create gym"""
        attendance = AttendanceFactory()
        attendance.create()
        temp_date_name = datetime.datetime.now()
        attendance.date = temp_date_name
        attendance.update()
        temp_attendance = Attendance.find(attendance.aid, attendance.gym_id)
        self.assertEqual(temp_attendance.date, temp_date_name)

    def test_read_attendances(self):
        """It should read all subscriptions"""
        temp_attendances_list = self._create_range(5)
        temp_list = Attendance.all(temp_attendances_list[0].pid,temp_attendances_list[0].gym_id)
        for i in range(4):
            self.assertEqual(temp_list[i].serialize(), temp_attendances_list[i].serialize())


