from flask import make_response, jsonify
from marshmallow import ValidationError

from src.attedence.attendance_model import Attendance
from src.attedence.attendance_validation import AttendanceBaseSchema
from src.common import status

attendance_schema = AttendanceBaseSchema()


class AttendanceService:

    @staticmethod
    def create_attendance_use_case(json):
        """Creates attendance"""
        try:
            data = attendance_schema.load(json)
            if not Attendance.check_if_exist(data['aid'], data['gym_id']):
                attendance = Attendance.create_model()
                attendance.deserialize(data)
                attendance.create()
                return make_response(jsonify({"result": "Created successfully", "message": f"{attendance._id}"}),
                                     status.HTTP_201_CREATED)
            return make_response(jsonify({"result": "Conflict Exception", "message": "this record is already exists"}),
                                 status.HTTP_409_CONFLICT)
        except ValidationError as err:
            return make_response(jsonify(err.messages),
                                 status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def update_attendance_use_case(json):
        """update attendance"""
        try:
            data = attendance_schema.load(json)
            if Attendance.find(data['aid'], data["gym_id"]) is not None:
                attendance = Attendance.create_model()
                attendance.deserialize(data)
                attendance.update()
                return make_response(jsonify({"result": "Updated successfully", "message": f"{attendance.id}"}),
                                     status.HTTP_200_OK)
            return make_response(jsonify({"result": "Not found Exception", "message": "this record is not exists"}),
                                 status.HTTP_404_NOT_FOUND)
        except ValidationError as err:
            return make_response(jsonify(err.messages),
                                 status.HTTP_406_NOT_ACCEPTABLE)

    @staticmethod
    def read_attendances_use_case(pid, gym_id):
        """Reads All attendance  for player subscription"""
        attendances = Attendance.all(pid, gym_id)
        if len(attendances) > 0:
            attendances_dict = [attendance.serialize() for attendance in attendances]
            return make_response(jsonify(attendances_dict),
                                 status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any payments"}),
                             status.HTTP_204_NO_CONTENT)



