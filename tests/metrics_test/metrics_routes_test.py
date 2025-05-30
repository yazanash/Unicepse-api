import unittest

from src.metrics.metrics_model import Metric
from tests.factories import MetricsFactory
from src.common import status
from app import app
from db import db


METRICS_URL = "/metrics"
dt_node = "metrics"
test_gym_id = 18

json_type = "application/json"


class TestMetricsRoutes(unittest.TestCase):
    """Test Suite for metrics route"""

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
        db.metrics.delete_many({})

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_metrics(self, count):
        """Factory method to create accounts in bulk"""
        metrics = []
        for _ in range(count):
            metric = MetricsFactory()
            metric.gym_id = test_gym_id
            metric.pid = 123456789
            response = self.client.post(METRICS_URL, json=metric.serialize(), content_type=json_type)
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test metric",
            )
            metrics.append(metric)
        return metrics

    ######################################################################
    #  T E S T   P L A Y E R   R O U T E S
    ######################################################################
    def test_create_metrics_route(self):
        """It should CREATE metrics through route service"""
        metric = MetricsFactory()
        metric.gym_id = test_gym_id
        metric.id = 10

        resp = self.client.post(
            METRICS_URL,
            json=metric.serialize(),
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_bad_request(self):
        """It should check for valid data on create route"""
        resp = self.client.post(METRICS_URL, json={'height': "not enough data"}, content_type=json_type)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_read_single_metrics_route(self):
        """It should READ subscription through route service"""
        metrics_list = self._create_metrics(3)
        resp1 = self.client.get(f"{METRICS_URL}/{metrics_list[0].gym_id}/{metrics_list[0].pid}/"
                                f"{metrics_list[0].id}")
        self.assertEqual(resp1.get_json()["pid"], metrics_list[0].pid)

        resp2 = self.client.get(f"{METRICS_URL}/{metrics_list[1].gym_id}/{metrics_list[1].pid}/"
                                f"{metrics_list[1].id}")
        self.assertEqual(resp2.get_json(), metrics_list[1].serialize())

        resp3 = self.client.get(f"{METRICS_URL}/{metrics_list[2].gym_id}/{metrics_list[2].pid}/"
                                f"{metrics_list[2].id}")
        self.assertEqual(resp3.get_json(), metrics_list[2].serialize())

    def test_read_metrics_route(self):
        """It should READ metrics through route service"""
        metrics_list = self._create_metrics(5)
        resp1 = self.client.get(f"{METRICS_URL}/{metrics_list[0].gym_id}/{metrics_list[0].pid}")
        print(resp1.get_json())
        for i in range(4):
            self.assertEqual(metrics_list[i].serialize(), resp1.get_json()[i])

    def test_read_bad_request(self):
        """It should check for valid id on READ metrics"""
        resp = self.client.get(f"{METRICS_URL}/18")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_metrics_route(self):
        """It should UPDATE metrics through route service"""
        metrics_list = self._create_metrics(1)
        metrics = metrics_list[0]
        height = metrics.height
        metrics.height = 750000.00
        resp = self.client.put(
            METRICS_URL,
            json=metrics.serialize(),
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        response = self.client.get(f"{METRICS_URL}/{metrics.gym_id}/{metrics.pid}/{metrics.id}")
        temp = Metric.create_model()
        temp.deserialize(response.get_json())
        self.assertEqual(temp.height, metrics.height)
        self.assertNotEqual(temp.height, height)

    def test_update_bad_request(self):
        """It should check for valid data in update metrics"""
        self._create_metrics(1)
        resp = self.client.put(
            METRICS_URL,
            json={'height': 'not enough data'},
            content_type=json_type
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
