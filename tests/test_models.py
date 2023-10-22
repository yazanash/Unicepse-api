"""
This class Tests Fake Module
"""
import time
import unittest
import logging
from . import factories as fake
from datetime import datetime
from src.common.utils import OtpHelper

logger = logging.getLogger(__name__)


################################################################
#   F A C T O R I E S   M O D E L   T E S T   C A S E S
################################################################
class TestFakes(unittest.TestCase):
    """Test Suite for Account feature"""
    ######################################################################
    #  T E S T   C A S E S
    ######################################################################
    def test_fake_training(self):
        """It should make a fake Training"""
        training = fake.TrainingFactory()
        logger.info("Testing fake training!")
        self.assertIsNotNone(training.id, f"training.id: {training.id}")
        self.assertIsNotNone(training.name, f"training.name: {training.name}")
        self.assertIsNotNone(training.images, f"training.images: {training.images}")
        print("Training: ", training.to_json())

    def test_fake_training_program(self):
        """It should make a fake Training program"""
        training_prog = fake.TrainingProgFactory()
        logger.info("Testing fake training program")
        self.assertIsNotNone(training_prog.id, f"trainingProgram.id: {training_prog.id}")
        print("Training Program: ", training_prog.id)

    def test_fake_Subscription(self):
        """It should make a fake Subscription"""
        subs = fake.SubscriptionFactory()
        logger.info("Testing fake subscription")
        self.assertIsNotNone(subs.id, f"")
        self.assertIsNotNone(subs.pl_id, f"")
        self.assertIsNotNone(subs.sp_id, f"")
        self.assertIsNotNone(subs.tr_id, f"")
        self.assertIsNotNone(subs.startDate, f"")
        self.assertIsNotNone(subs.endDate, f"")
        self.assertIsNotNone(subs.price, f"")
        self.assertIsNotNone(subs.priceAD, f"")
        self.assertIsNotNone(subs.isD, f"")
        self.assertIsNotNone(subs.isPay, f"")
        self.assertIsNotNone(subs.paymentTotal, f"")
        self.assertIsNotNone(subs.discountValue, f"")
        self.assertIsNotNone(subs.discountDes, f"")
        print("Subscription: ", subs.to_json())

    def test_fake_player(self):
        """It should make a fake Player"""
        player = fake.PlayerFactory()
        logger.info("Testing fake Player!")
        self.assertIsNotNone(player)

    def test_otp_helper(self):
        """It should generate multi-otp and validate them"""
        otp_helper = OtpHelper()
        res1 = otp_helper.generate_otp()
        res2 = otp_helper.generate_otp()
        time.sleep(15)
        self.assertTrue(otp_helper.validate_otp(res1))
        self.assertTrue(otp_helper.validate_otp(res2))


################################################################
#   D A T A B A S E   M O D E L   T E S T   C A S E S
################################################################
class TestDatabase(unittest.TestCase):
    """
    Testcases for firebase database:
        * Create
        * READ
        * UPDATE
        * DELETE
    """
    ######################################################################
    #  T E S T   C A S E S
    ######################################################################
    def test_sample(self):
        """@TODO: Delete this testcase"""
        self.assertEqual(True, True)
