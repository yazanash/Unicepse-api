import logging
from db import db
from src.common.utils import logger
from bson.json_util import dumps, loads

class PaymentPersistentBase:
    """
    Base class added persistent methods

    SNode = Static Node
    Map:
    Gyms: (SNode)
        gym_id:
            Players: (SNode)
                pl_id:
                    Subs: (SNode)
                        sub_id:
                            Payments: (SNode)
                                pay_id: VALUE
    """

    def create(self):
        """
        Creates a Payment in the database
        """
        logger.info("Creating Payment in subscription= %s", self.sub_id)

        payments = db["Gyms"][self.gym_id]["Players"][self.pl_id]["Subs"][self.sub_id]["Payments"]
        print("create in persistent: ", type(payments))
        payments.insert_one(self.serialize())

        logger.info("Payment %s Created successfully", self.sub_id)

    def update(self):
        """
        Updates a Player to the database
        """
        logger.info("Updating Payment: %s", self.id)

        payments = db["Gyms"][self.gym_id]["Players"][self.pl_id]["Subs"][self.sub_id]["Payments"]

        res = payments.update_one({"id": self.id}, {"$set": self.serialize()})
        if res.modified_count == 1:
            logger.info("Payment %s Updated successfully", self.id)
        else:
            logger.info("Payment %s could NOT be Updated ", self.id)

    def delete(self):
        """Removes a Player from the data store"""
        logger.info("Deleting %s", self.id)

        payments = db["Gyms"][self.gym_id]["Players"][self.pl_id]["Subs"][self.sub_id]["Payments"]
        res = payments.delete_one({"id": self.id})
        if res.deleted_count == 1:
            logger.info("Payment %s Deleted successfully", self.id)
        else:

            logger.info("Payment %s could NOT be Deleted", self.id)

    @classmethod
    def all(cls, gym_id, pl_id, sub_id):
        """Returns all the records in the database"""
        logger.info("Processing all Player-transaction records")

        payments = db["Gyms"][gym_id]["Players"][pl_id]["Subs"][sub_id]["Payments"].find()
        data = []
        pays = loads(dumps(payments))
        if pays is not None:
            for val in pays:
                if val is not None:
                    print("payments in all(): ", type(pays), pays)
                    print("val in all(): ", type(val), val)

                    pay = cls.deserialize(val)
                    data.append(pay)
        return data

    @classmethod
    def all_json(cls, gym_id, pl_id, sub_id):
        """Returns all the records in the database"""
        logger.info("Processing all Player-transaction records")
        payments = db["Gyms"][gym_id]["Players"][pl_id]["Subs"][sub_id]["Payments"].find()
        if payments is not None:
            for val in payments:
                if val is not None:
                    logger.info("Val in ref: %s", val)
            return dumps(payments)
        return []

    @classmethod
    def check_if_exist(cls, gym_id, pl_id, sub_id, id):
        """check if record is exist in database"""
        logger.info("check if data exist")

        payment = db["Gyms"][gym_id]["Players"][pl_id]["Subs"][sub_id]["Payments"].find({"id": id})
        if payment is not None:
            return True
        return False

    @classmethod
    def find(cls, gym_id, player_id, sub_id, uid):
        """Finds a record by its ID"""
        logger.info("Processing lookup for id %s ...", id)

        payment = db["Gyms"][gym_id]["Players"][player_id]["Subs"][sub_id]["Payments"].find_one({"id": uid})
        if payment is not None:
            pays = loads(dumps(payment))
            if pays is not None:
                print("Pays in find(): ", type(pays), pays)
                pay = cls.deserialize(pays)
                return pay

        return None
