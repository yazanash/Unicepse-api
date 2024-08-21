import datetime
import unittest

from src.attedence.attendance_model import Attendance
from tests.factories import AttendanceFactory
from src.common import status
from app import app
from db import db


ATTENDANCES_URL = "/api/v1/attendances"
dt_node = "attendances"

json_type = "application/json"


class TestAttendanceRoutes(unittest.TestCase):
    """Test Suite for attendances route"""

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
        db.attendances.delete_many({})

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_attendance(self, count):
        """Factory method to create accounts in bulk"""
        attendances = []
        for _ in range(count):
            attendance = AttendanceFactory()
            response = self.client.post(ATTENDANCES_URL, json=attendance.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Account",
            )
            attendances.append(attendance)
        return attendances

    ######################################################################
    #  T E S T   A T T E N D A N C E   R O U T E S
    ######################################################################
    def test_create_attendance_route(self):
        """It should CREATE attendance through route service"""
        attendance = AttendanceFactory()
        resp = self.client.post(
            ATTENDANCES_URL,
            json=attendance.serialize(),
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_bad_request(self):
        """It should check for valid data on create route"""
        resp = self.client.post(ATTENDANCES_URL, json={'gym': "not enough data"}, content_type=json_type)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_read_attendance_route(self):
        """It should READ all attendance through route service"""
        attendances_list = self._create_attendance(5)
        resp1 = self.client.get(f"{ATTENDANCES_URL}")
        for i in range(4):
            self.assertEqual(attendances_list[i].serialize(), resp1.get_json()[i])

    def test_read_bad_request(self):
        """It should check for valid id on READ gym"""
        resp = self.client.get(f"{ATTENDANCES_URL}/1599999")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_attendance_route(self):
        """It should UPDATE attendances through route service"""
        attendances_list = self._create_attendance(1)
        attendance = attendances_list[0]
        date = attendance.date
        attendance.date = datetime.datetime.now()
        resp = self.client.put(
            ATTENDANCES_URL,
            json=attendance.serialize(),
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        response = self.client.get(f"{ATTENDANCES_URL}/{attendance.gym_id}/{attendance.aid}")
        temp = Attendance.create_model()
        temp.deserialize(response.get_json())
        self.assertEqual(temp.date, attendance.date)
        self.assertNotEqual(temp.date, date)

    def test_update_bad_request(self):
        """It should check for valid data in update player"""
        self._create_attendance(1)
        resp = self.client.put(
            ATTENDANCES_URL,
            json={'gym_name': 'not enough data'},
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_406_NOT_ACCEPTABLE)
