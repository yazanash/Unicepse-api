from src.attedence import attendance_persistant_base


class Attendance(attendance_persistant_base.AttendancePersistentBase):
    def __init__(self,
                 aid=None,
                 _id=None,
                 date=None,
                 login_time=None,
                 logout_time=None,
                 pid=None,
                 sid=None,
                 gym_id=None,
                 taken_key=None,
                 is_logged=None,
                 ):
        self.aid = aid
        self._id = _id
        self.date = date
        self.login_time = login_time
        self.logout_time = logout_time
        self.pid = pid
        self.sid = sid
        self.gym_id = gym_id
        self.taken_key = taken_key
        self.is_logged = is_logged

    def serialize(self):
        """should return json map for this model"""
        return {
            'id': str(self._id),
            'aid': self.aid,
            'date': self.date,
            'login_time': self.login_time,
            'logout_time': self.logout_time,
            'pid': self.pid,
            'sid': self.sid,
            'gym_id': self.gym_id,
            'taken_key': self.taken_key,
            'is_logged': self.is_logged,
        }

    def serialize_to_db(self):
        """should return json map for this model"""
        return {
            'aid': self.aid,
            'date': self.date,
            'login_time': self.login_time,
            'logout_time': self.logout_time,
            'pid': self.pid,
            'sid': self.sid,
            'gym_id': self.gym_id,
            'taken_key': self.taken_key,
            'is_logged': self.is_logged,
        }

    def deserialize(self, json):
        """should return this model from dict"""
        self.aid = json["aid"]
        self.date = json["date"]
        self.login_time = json["login_time"]
        self.logout_time = json["logout_time"]
        self.pid = json["pid"]
        self.sid = json["sid"]
        self.gym_id = json["gym_id"]
        self.taken_key = json["taken_key"]
        self.is_logged = json["is_logged"]

    def deserialize_from_db(self, json):
        """should return this model from dict"""
        self._id = json.get("_id")
        self.aid = json["aid"]
        self.date = json["date"]
        self.login_time = json["login_time"]
        self.logout_time = json["logout_time"]
        self.pid = json["pid"]
        self.sid = json["sid"]
        self.gym_id = json["gym_id"]
        self.taken_key = json["taken_key"]
        self.is_logged = json["is_logged"]

    @staticmethod
    def create_model():
        return Attendance()