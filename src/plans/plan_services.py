from bson import ObjectId
from flask import make_response, jsonify
from marshmallow import ValidationError

from src.gym.gym_model import Gym
from src.common import status
from src.plans.plan_model import Plan
from src.plans.plan_validation import PlanBaseSchema

plan_schema = PlanBaseSchema()


class PlanService:

    @staticmethod
    def create_plan_use_case(json):
        """Creates plan"""
        try:
            data = plan_schema.load(json)
            if not Plan.check_if_exist(data['plan_name']):
                plan = Plan.create_model()
                plan.deserialize(data)
                plan.create()
                return make_response(jsonify({"result": "Created successfully", "message": f"{plan.id}"}),
                                     status.HTTP_201_CREATED)
            return make_response(jsonify({"result": "Conflict Exception", "message": "this record is already exists"}),
                                 status.HTTP_409_CONFLICT)
        except ValidationError as err:
            return make_response(jsonify(err.messages),
                                 status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def update_plan_use_case(json,plan_id):
        """update plan"""
        try:
            data = plan_schema.load(json)
            plan = Plan.find(plan_id)
            if plan is not None:
                plan.deserialize(data)
                plan.update()
                return make_response(jsonify({"result": "Updated successfully", "message": f"{plan.id}"}),
                                     status.HTTP_200_OK)
            return make_response(jsonify({"result": "Not found Exception", "message": "this record is not exists"}),
                                 status.HTTP_404_NOT_FOUND)
        except ValidationError as err:
            return make_response(jsonify(err.messages),
                                 status.HTTP_406_NOT_ACCEPTABLE)

    @staticmethod
    def read_plan_use_case(plan_id):
        """Reads All payments  for player subscription"""
        if ObjectId.is_valid(plan_id):
            plan = Plan.find(plan_id)
            if plan is not None:
                return make_response(jsonify(plan.serialize()),
                                     status.HTTP_200_OK)
            return make_response(jsonify({"result": "No content", "message": "cannot found any plans"}),
                                 status.HTTP_404_NOT_FOUND)
        else:
            return make_response(jsonify({"result": "No content", "message": "cannot found any plans with this id"}),
                                 status.HTTP_404_NOT_FOUND)

    @staticmethod
    def read_plans_use_case():
        """Reads All payments  for player subscription"""
        plans = Plan.all()
        if len(plans) > 0:
            plans_dict = [plan.serialize() for plan in plans]
            return make_response(jsonify(plans_dict),
                                 status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any plans"}),
                             status.HTTP_204_NO_CONTENT)



