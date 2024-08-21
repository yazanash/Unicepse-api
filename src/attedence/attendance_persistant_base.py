from db import db
from src.common.utils import logger


class AttendancePersistentBase:
    """
    Base class added persistent methods
    """

    def create(self):
        """
        Creates a gym in the database
        """
        logger.info("Creating attendance  %s", self.aid)

        attendances = db.attendances.insert_one(self.serialize_to_db())
        self._id = attendances.inserted_id
        logger.info("attendance %s Created successfully", self._id)

    def update(self):
        """
        Updates a gym to the database
        """
        logger.info("Updating attendance: %s", self.aid)
        attendances = db.attendances
        res = attendances.update_one(
            {"aid": self.aid, "gym_id": self.gym_id},
            {'$set': self.serialize()}
        )
        if res.modified_count == 1:
            logger.info("attendance: %s Updated successfully", self.aid)
        else:
            logger.info("attendance: %s could NOT be Updated ", self.aid)

    @classmethod
    def all(cls, pid, gym_id):
        """Returns all the records in the database"""
        logger.info("Processing all gyms records")
        attendances = db.attendances.find({"aid": pid, "gym_id": gym_id})
        data = []
        if attendances is not None:
            for val in attendances:
                if val is not None:
                    attendance = cls.create_model()
                    attendance.deserialize_from_db(val)
                    data.append(attendance)
        return data

    @classmethod
    def check_if_exist(cls, aid, gym_id):
        """check if record is exist in database"""
        logger.info("check if data exist")
        attendance = db.attendances.find_one({"aid": aid, "gym_id": gym_id})
        if attendance is not None:
            return True
        return False

    @classmethod
    def find(cls, aid, gym_id):
        """Finds a record by its ID"""
        logger.info("Processing lookup for id %s ...", aid)
        attendances = db.attendances.find_one({'aid': aid, "gym_id": gym_id})
        if attendances is not None:
            attendance = cls.create_model()
            attendance.deserialize_from_db(attendances)
            return attendance
        return None
