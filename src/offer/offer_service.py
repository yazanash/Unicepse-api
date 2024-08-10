from bson import ObjectId
from flask import make_response, jsonify
from marshmallow import ValidationError

from src.offer.offer_model import Offer
from src.offer.offer_validation import OfferBaseSchema
from src.gym.gym_model import Gym
from src.common import status
from src.plans.plan_model import Plan
from src.plans.plan_validation import PlanBaseSchema


offer_schema = OfferBaseSchema()


class OfferService:

    @staticmethod
    def create_offer_use_case(json):
        """Creates offer"""
        try:
            data = offer_schema.load(json)
            if not Offer.check_if_exist(data['offer_name']):
                offer = Offer.create_model()
                offer.deserialize(data)
                offer.create()
                return make_response(jsonify({"result": "Created successfully", "message": f"{offer.id}"}),
                                     status.HTTP_201_CREATED)
            return make_response(jsonify({"result": "Conflict Exception", "message": "this record is already exists"}),
                                 status.HTTP_409_CONFLICT)
        except ValidationError as err:
            return make_response(jsonify(err.messages),
                                 status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def update_offer_use_case(json, offer_id):
        """update offer"""
        try:
            data = offer_schema.load(json)
            offer = Offer.find(offer_id)
            if offer is not None:
                offer.deserialize(data)
                offer.update()
                return make_response(jsonify({"result": "Updated successfully", "message": f"{offer.id}"}),
                                     status.HTTP_200_OK)
            return make_response(jsonify({"result": "Not found Exception", "message": "this record is not exists"}),
                                 status.HTTP_404_NOT_FOUND)
        except ValidationError as err:
            return make_response(jsonify(err.messages),
                                 status.HTTP_406_NOT_ACCEPTABLE)

    @staticmethod
    def read_offer_use_case(offer_id):
        """Reads All offers"""
        if ObjectId.is_valid(offer_id):
            offer = Offer.find(offer_id)
            if offer is not None:
                return make_response(jsonify(offer.serialize()),
                                     status.HTTP_200_OK)
            return make_response(jsonify({"result": "No content", "message": "cannot found any offer"}),
                                 status.HTTP_404_NOT_FOUND)
        else:
            return make_response(jsonify({"result": "No content", "message": "cannot found any offer with this id"}),
                                 status.HTTP_404_NOT_FOUND)

    @staticmethod
    def read_offers_use_case():
        """Reads All offer"""
        offers = Offer.all()
        if len(offers) > 0:
            offers_dict = [offer.serialize() for offer in offers]
            return make_response(jsonify(offers_dict),
                                 status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any plans"}),
                             status.HTTP_204_NO_CONTENT)



