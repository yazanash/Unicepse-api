import unittest
from db import db
from src.metrics.metrics_model import Metric
from api.tests.factories import MetricsFactory


class TestMetrics(unittest.TestCase):
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
        db.metrics.delete_many({})

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_range(self, count):
        """Helper method for creating Metrics in bulk"""
        
        metrics = []
        for _ in range(count):
            met = MetricsFactory()
            met.pid = 123456789
            met.gym_id = 18
            met.create()
            metrics.append(met)
        return metrics

    ######################################################################
    #  T E S T   P A Y M E N T   M O D E L
    ######################################################################

    def test_serialize_Metric(self):
        """It should serialize a subscription"""
        met = MetricsFactory()
        serialized = met.serialize()

        self.assertEqual(serialized['id'], met.id)
        self.assertEqual(serialized['pid'], met.pid)
        self.assertEqual(serialized['gym_id'], met.gym_id)
        self.assertEqual(serialized['check_date'], met.check_date.strftime("%d/%m/%Y"))

    def test_deserialize_Metric(self):
        """It should deserialize a Metric"""
        met = MetricsFactory()
        deserialized = Metric.create_model()
        deserialized.deserialize(met.serialize())
        self.assertEqual(deserialized.pid, met.pid)
        self.assertEqual(deserialized.gym_id, met.gym_id)
        self.assertEqual(deserialized.check_date.strftime("%d/%m/%Y"), met.check_date.strftime("%d/%m/%Y"))

    def test_create_Metric(self):
        """It should create subscription with no Metrics"""
        metric = MetricsFactory()
        metric.create()
        temp_met = Metric.find(metric.gym_id, metric.pid, metric.id)
        self.assertEqual(temp_met.check_date.strftime("%d/%m/%Y"), metric.check_date.strftime("%d/%m/%Y"))

    def test_read_all_Metrics(self):
        """It should read all metrics"""
        met_list = self._create_range(4)
        pid = met_list[0].pid
        gym_id = met_list[0].gym_id
        temp_list = Metric.all(gym_id, pid)

        for i in range(4):
            self.assertEqual(temp_list[i].serialize(), met_list[i].serialize())

    def test_read_single_Metrics(self):
        """It should read single metrics"""
        met_list = self._create_range(1)
        pid = met_list[0].pid
        gym_id = met_list[0].gym_id
        temp = Metric.find(gym_id, pid, met_list[0].id)
        self.assertEqual(temp.serialize(), met_list[0].serialize())

    def test_update_Metric(self):
        """It should update subscription """
        met = MetricsFactory()
        met.create()
        met.height = 1500.00
        met.update()
        temp_sub = Metric.find(met.gym_id, met.pid, met.id)
        self.assertEqual(temp_sub.height, 1500.00)

