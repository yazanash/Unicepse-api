from src.routine.routine_service import RoutineServiceBase
from src.common import errors
from src.common.utils import logger


class Routine (RoutineServiceBase):

    def __init__(self,
                 id=None,
                 pid=None,
                 routine_no=None,
                 routine_date=None,
                 days_group_map=None,
                 routine_items=None,
                 gym_id=None,
                 ):
        super().__init__()
        self.rid = id
        self.pid = pid
        self.gym_id = gym_id
        self.routine_no = routine_no,
        self.routine_date = routine_date
        self.days_group_map = days_group_map
        self.routine_items = routine_items

    def deserialize(self, json):
        """ deserialize player routine data  """
        try:
            logger.info("deserialize player routine")
            self.rid = json["rid"]
            self.pid = json["pid"]
            self.routine_no = json["routine_no"],
            self.routine_date = json["routine_date"]
            self.days_group_map = json["days_group_map"]
            self.routine_items = json["routine_items"]
        except AttributeError as e:
            logger.error("Error deserializing player routine : %s", e)
            raise errors.DataValidationError("Player routine deserializing Error!")
        except TypeError as e:
            logger.error("Type Error deserialize player routine : %s", e)

    def serialize(self):
        """serialize player routine data """
        try:
            logger.info("serialize player routine")
            mapping = {
                "rid": self.rid,
                "pid": self.pid,
                "routine_no": self.routine_no,
                "routine_date": self.routine_date,
                "days_group_map": self.days_group_map,
                "routine_items": self.routine_items,
            }
            return mapping
        except AttributeError as e:
            logger.error("Error serializing player routine error : %s", e)
            raise errors.DataValidationError

    @staticmethod
    def create_model():
        return Routine()
