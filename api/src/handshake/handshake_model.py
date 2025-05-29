from src.handshake import handshake_persistent_base


class HandShake(handshake_persistent_base.HandShakePersistentBase):
    def __init__(self,
                 uid=None,
                 pid=None,
                 gym_id=None,
                 created_at=None,
                 status=None,
                 ):
        self.uid = uid
        self.pid = pid
        self.gym_id = gym_id
        self.created_at = created_at,
        self.status = status,

    def serialize(self):
        """should return json map for this model"""
        return {
            'uid': self.uid,
            'pid': self.pid,
            'gym_id': self.gym_id,
            'created_at': self.created_at,
            'status': self.status,
        }

    def deserialize(self, json):
        """should return this model from dict"""
        self.uid = json["uid"]
        self.pid = json["pid"]
        self.gym_id = json["gym_id"]

    def deserialize_from_db(self, json):
        """should return this model from dict"""
        self.uid = json["uid"]
        self.pid = json["pid"]
        self.gym_id = json["gym_id"]
        self.created_at = json['created_at']
        self.status = json['status']

    @staticmethod
    def create_model():
        return HandShake()
