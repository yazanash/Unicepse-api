"""
This class Tests Fake Module
"""
import time
import unittest
import logging
from . import factories as fake
from datetime import datetime
from src.common.utils import OtpHelper, TokenGenerator

logger = logging.getLogger(__name__)


################################################################
#   F A C T O R I E S   M O D E L   T E S T   C A S E S
################################################################
class TestFakes(unittest.TestCase):
    """Test Suite for Fakes & Factories"""
    ######################################################################
    #  T E S T   C A S E S
    ######################################################################
    def test_fake_training(self):
        """It should make a fake Training"""
        training = fake.TrainingFactory()
        logger.info("Testing fake training!")
        self.assertIsNotNone(training.id, f"training.id: {training.id}")
        self.assertIsNotNone(training.name, f"training.name: {training.name}")
        self.assertIsNotNone(training.image_url, f"training.images: {training.image_url}")
        print("Training: ", training.serialize())

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

    def test_otp_helper_class(self):
        """It Should generate and validate and flush otp-stack"""
        otph = OtpHelper()
        res1 = otph.generate(interval=5)
        res2 = otph.generate(interval=5)
        #   assert two otp(s) are different and added to stack
        self.assertNotEquals(res1, res2)
        self.assertTrue(otph.verify(res1))
        self.assertTrue(otph.verify(res2))
        self.assertEqual(len(otph.otp_list), 2)
        print(res1, res2)
        time.sleep(5)
        #   assert otp(s) are not valid after time interval
        self.assertEqual(otph.verify(res1), False)
        self.assertEqual(otph.verify(res2), False)
        res3 = otph.generate(interval=5)
        #   assert stack is flushed on new generation
        self.assertEqual(len(otph.otp_list), 1)

    def test_otp_helper_multi_generation(self):
        """It should generate multi-otp and validate them"""
        otp_helper = OtpHelper()
        res1 = otp_helper.generate()
        time.sleep(5)
        res2 = otp_helper.generate()
        print(res1, res2)
        self.assertNotEquals(res1, res2)
        self.assertTrue(otp_helper.verify(res1))
        self.assertTrue(otp_helper.verify(res2))

    def test_token_generator(self):
        """It should make unique tokens"""
        token1 = TokenGenerator.generate_token()
        token2 = TokenGenerator.generate_token()
        self.assertNotEquals(token1, token2)


################################################################
#   D A T A B A S E   M O D E L S   T E S T   C A S E S
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

