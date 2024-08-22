from flask import make_response, jsonify

from src.handshake.handshake_model import HandShake
from src.metrics.metrics_validator import validate_metric
from src.metrics.metrics_model import Metric
from src.common import status
from src.common.errors import DataValidationError


class MetricsService:

    @staticmethod
    def create_metric_use_case(json):
        """Creates metric for player"""
        try:
            validate_metric(json)
            if not Metric.check_if_exist(json['gym_id'], json['pid'], json['id']):
                metric = Metric.create_model()
                metric.deserialize(json)
                metric.create()
                return make_response(jsonify({"result": "Created successfully", "message": f"{metric.id}"}),
                                     status.HTTP_201_CREATED)
            return make_response(
                jsonify({"result": "Conflict Exception", "message": "this record is already exists"}),
                status.HTTP_409_CONFLICT)
        except DataValidationError:
            return make_response(jsonify({"result": "Validation Error", "message": "required data is missing "}),
                                 status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def read_metrics_use_case(current_user):
        """Reads all metrics for player"""
        user_handshake_data = HandShake.all(current_user.uid)
        if len(user_handshake_data) > 0:
            data = {}
            for handshake in user_handshake_data:
                metrics_list = Metric.all(handshake.gym_id, handshake.pid)
                if len(metrics_list) > 0:
                    for metric in metrics_list:
                        data.update(metric.serialize())
                else:
                    return make_response(jsonify({"result": "No content", "message": "cannot found any metrics"}),
                                         status.HTTP_204_NO_CONTENT)
            return make_response(jsonify(data),
                                 status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any handshakes"}),
                             status.HTTP_204_NO_CONTENT)

    @staticmethod
    def read_single_metrics_use_case(gym_id, pid, id):
        """Reads single metrics for player"""
        metric = Metric.find(gym_id, pid, id)
        if metric is not None:
            return make_response(jsonify(metric.serialize()),
                                 status.HTTP_200_OK)
        return make_response(jsonify({"result": "No content", "message": "cannot found any metrics"}),
                             status.HTTP_204_NO_CONTENT)

    @staticmethod
    def update_metric_use_case(json):
        """Updates a record for player"""
        try:
            validate_metric(json)
            res = Metric.find(json['gym_id'], json['pid'], json['id'])
            if not res:
                return make_response(jsonify({"result": "Not found", "message": "this metric is not exist"}),
                                     status.HTTP_404_NOT_FOUND)
            res.deserialize(json)
            res.update()
            return make_response(
                jsonify({"result": "Updated successfully", "message": "metric updated successfully"}),
                status.HTTP_200_OK)
        except DataValidationError:
            return make_response(jsonify({"result": "Validation Error",
                                          "message": "required data is missing "}),
                                 status.HTTP_400_BAD_REQUEST)
