from src.Training.training_service import RoutineServiceBase
from src.common import errors
from src.common.utils import logger


class Routine (RoutineServiceBase):

    def __init__(self,
                 lid=None,
                 pid=None,
                 routine_no=None,
                 routine_date=None,
                 days_group_map=None,
                 routine_items=None,
                 gym_id=None,
                 ):
        super().__init__()
        self.lid = lid
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
            self.lid = json["RoutineId"]
            self.pid = json["pid"]
            self.routine_no = json["RoutineNumber"],
            self.routine_date = json["RoutineDate"]
            self.days_group_map = json["GroupMapping"]
            self.routine_items = json["Schedule"]
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
                "RoutineId": self.lid,
                "pid": self.pid,
                "RoutineNumber": self.routine_no,
                "RoutineDate": self.routine_date,
                "GroupMapping": self.days_group_map,
                "Schedule": self.routine_items,
            }
            return mapping
        except AttributeError as e:
            logger.error("Error serializing player routine error : %s", e)
            raise errors.DataValidationError

    @staticmethod
    def create_model():
        return Routine()
