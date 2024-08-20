from flask import make_response, jsonify

from src.common.errors import *
from src.common import status
from .routine_model import Routine


class RoutineService:

    @staticmethod
    def create_routine_use_case(json):
        """Creates Subscription-subscription for player"""
        try:
            if not Routine.check_if_exist(json['gym_id'], json['pid'], json['rid']):
                routine = Routine.create_model()
                routine.deserialize(json)
                routine.create()
                return make_response(jsonify({"result": "Created successfully", "message": f"{routine.rid}"}),
                                     status.HTTP_201_CREATED)
            return make_response(jsonify({"result": "Conflict Exception", "message": "this record is already exists"}),
                                 status.HTTP_409_CONFLICT)
        except DataValidationError:
            return make_response(jsonify({"result": "Validation Error", "message": "required data is missing "}),
                                 status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def read_routine_use_case(gym_id, pid):
        """Reads All Subscription-subscription for player"""
        routine = Routine.find(gym_id, pid).sort('routine_date', -1).limit(1).next()
        if routine is not None:
            return make_response(jsonify(routine.serialize()),
                                 status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any transactions"}),
                             status.HTTP_204_NO_CONTENT)

    @staticmethod
    def update_routine_use_case(data):
        """update subscription for player"""
        routine = Routine.find_by_rid(data['gym_id'], data['pid'], data['id'])
        if not routine:
            return make_response(jsonify({"result": "Not found", "message": "this transaction is not exist"}),
                                 status.HTTP_404_NOT_FOUND)
        sub = Routine.create_model()
        sub.deserialize(data)
        sub.update()
        return make_response(jsonify({"result": "Updated successfully", "message": "subscription updated successfully "}),
                             status.HTTP_200_OK)


