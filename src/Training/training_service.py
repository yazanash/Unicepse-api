from src.common.utils import logger
from db import db

dt_node = "routines"


class RoutineServiceBase:
    """Base class added persistent methods"""

    def create(self):
        """
        Creates a Player to the database
        """
        logger.info("Creating %s", self.routine_no)
        routine_path = db["Gyms"][self.gym_id][dt_node]
        routine_path.insert_one(self.serialize())
        logger.info("Created successfully %s", self.routine_no)

    def update(self):
        """
        Updates a Player to the database
        """
        logger.info("Updating %s", self.routine_no)
        routine_path = db["Gyms"][self.gym_id][dt_node]
        routine_path.update_one({'RoutineId': self.lid}, {'$set': self.serialize()})
        logger.info("Updated Successfully %s", self.routine_no)

    @classmethod
    def all(cls, gym_id):
        """Returns all the records in the database"""

    @classmethod
    def find(cls, gym_id, by_uid):
        """Finds a record by its ID"""
        logger.info("Processing lookup for id %s ...", by_uid)
        try:
            data = db["Gyms"][gym_id][dt_node]
            routine_data = data.find_one({"RoutineId": by_uid})
            if routine_data is not None:
                routine = cls.create_model()
                routine.deserialize(routine_data)
                return routine
            else:
                return None
        except RoutineNotFoundError:
            return None

    @classmethod
    def check_if_exist(cls, gym_id, by_uid):
        """check if record is exist in database"""
        logger.info("check if data exist")
        data = db["Gyms"][gym_id][dt_node]
        routine_data = data.find_one({"RoutineId": by_uid})
        if routine_data is not None:
            return True
        return False


class RoutineNotFoundError(Exception):
    """Used for auth validation errors """
