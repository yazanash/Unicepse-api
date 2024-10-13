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
        routine_path = db.routines.insert_one(self.serialize())
        logger.info("Created successfully %s", self.routine_no)

    def update(self):
        """
        Updates a Player to the database
        """
        logger.info("Updating %s", self.routine_no)
        routine_path = db.routines
        routine_path.update_one({'rid': self.rid}, {'$set': self.serialize()})
        logger.info("Updated Successfully %s", self.routine_no)

    @classmethod
    def all(cls, gym_id, pid):
        """Returns all the records in the database"""
        logger.info("Processing all Player-Subscription records")

        routines_ref = db.routines.find({"pid": pid, "gym_id": gym_id})
        data = []
        if routines_ref is not None:
            for val in routines_ref:
                routine = cls.create_model()
                routine.deserialize(val)
                data.append(routine)
        return data

    @classmethod
    def find(cls, gym_id, pid):
        """Finds a record by its ID"""
        logger.info("Processing lookup for id %s ...", pid)
        try:
            routines = db.routines.find({"gym_id": gym_id, "pid": pid})
            documents = list(routines)
            if routines is not None and not documents:
                routine_data = db.routines.find({"gym_id": gym_id, "pid": pid}).sort('routine_date', -1).limit(1).next()
                if routine_data is not None:
                    routine = cls.create_model()
                    routine.deserialize(routine_data)
                    return routine
                else:
                    return None
            else:
                return None
        except RoutineNotFoundError:
            return None
        except StopIteration:
            return None

    @classmethod
    def find_by_rid(cls, gym_id, pid, rid):
        """Finds a record by its ID"""
        logger.info("Processing lookup for id %s ...", rid)
        try:
            data = db.routines
            routine_data = data.find_one({"rid": rid, "pid": pid, "gym_id": gym_id})
            if routine_data is not None:
                routine = cls.create_model()
                routine.deserialize(routine_data)
                return routine
            else:
                return None
        except RoutineNotFoundError:
            return None

    @classmethod
    def check_if_exist(cls, gym_id, pid, rid):
        """check if record is exist in database"""
        logger.info("check if data exist")
        data = db.routines
        routine_data = data.find_one({"rid": rid, "pid": pid, "gym_id": gym_id})
        if routine_data is not None:
            return True
        return False


class RoutineNotFoundError(Exception):
    """Used for auth validation errors """
