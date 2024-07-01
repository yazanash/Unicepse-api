import unittest
import db
from src.metrics.metrics_model import Metric
from .factories import MetricsFactory


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

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_range(self, count):
        """Helper method for creating Metrics in bulk"""
        
        metrics = []
        pl_id = MetricsFactory().pl_id
        gym_id = MetricsFactory().gym_id
        for _ in range(count):
            met = MetricsFactory()
            met.pl_id = pl_id
            met.gym_id = gym_id
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
        self.assertEqual(serialized['pl_id'], met.pl_id)
        self.assertEqual(serialized['gym_id'], met.gym_id)
        self.assertEqual(serialized['check_date'], met.check_date.strftime("%Y/%m/%d, %H:%M:%S"))

    def test_deserialize_Metric(self):
        """It should deserialize a Metric"""
        met = MetricsFactory()
        deserialized = Metric.deserialize(met.serialize())
        self.assertEqual(deserialized.pl_id, met.pl_id)
        self.assertEqual(deserialized.gym_id, met.gym_id)
        self.assertEqual(deserialized.check_date, met.check_date)

    def test_create_Metric(self):
        """It should create subscription with no Metrics"""
        metric = MetricsFactory()
        metric.create()
        temp_met = Metric.find(gym_id=metric.gym_id, pl_id=metric.pl_id, met_id=metric.id)
        self.assertEqual(temp_met['check_date'], metric.check_date.strftime("%Y/%m/%d, %H:%M:%S"))

    def test_read_all_Metrics(self):
        """It should read all subscriptions"""
        met_list = self._create_range(4)
        pl_id = met_list[0].pl_id
        gym_id = met_list[0].gym_id
        temp_list = Metric.all(gym_id, pl_id)

        for i in range(4):
            self.assertEqual(temp_list[i].serialize(), met_list[i].serialize())

    def test_update_Metric(self):
        """It should update subscription """
        met = MetricsFactory()
        met.create()
        met.height = 1500
        met.update()
        temp_sub = Metric.find(met.gym_id, met.pl_id, met.id)
        self.assertEqual(temp_sub['height'], 1500)

        met.height = 100
        met.update()
        temp_sub = Metric.find(met.gym_id, met.pl_id, met.id)
        self.assertEqual(temp_sub['height'], 100)

    def test_delete_Metric(self):
        """It should delete subscription"""
        met = MetricsFactory()
        met.create()
        met.delete()
        temp_sub = Metric.find(met.gym_id, met.pl_id, met.id)
        self.assertIsNone(temp_sub)
