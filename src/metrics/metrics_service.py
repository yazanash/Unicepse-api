from src.metrics.metrics_validator import validate_metric
from src.metrics.metrics_model import Metric
from src.common import status
from src.common.errors import DataValidationError


class MetricsService:

    @staticmethod
    def create_metric_usecase(json):
        """Creates metric for player"""
        try:
            validate_metric(json)
            if not Metric.check_if_exist(json['gym_id'], json['pl_id'], json['id']):
                metric = Metric.deserialize(json)
                metric.create()
                return status.HTTP_201_CREATED
            return status.HTTP_409_CONFLICT
        except DataValidationError:
            return status.HTTP_400_BAD_REQUEST

    @staticmethod
    def read_metrics_usecase(path: dict):
        """Reads all metrics for player"""
        res = Metric.all_json(path['gym_id'], path['pl_id'])
        if len(res) > 0:
            return {res.__str__()}, status.HTTP_200_OK
        return status.HTTP_204_NO_CONTENT

    @staticmethod
    def update_metric_usecase(json):
        """Updates a record for player"""
        res = Metric.find(json['gym_id'], json['pl_id'], json['id'])
        if not res:
            return status.HTTP_404_NOT_FOUND
        res.deserialize(json)
        res.update()
        return status.HTTP_200_OK

    @staticmethod
    def delete_metric_usecase(json):
        """Deletes a record of metrics"""
        res = Metric.find(json['gym_id'], json['pl_id'], json['id'])
        if not res:
            return status.HTTP_404_NOT_FOUND
        res.deserialize(json)
        res.delete()
        return status.HTTP_200_OK

