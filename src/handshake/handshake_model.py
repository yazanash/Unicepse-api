from src.handshake import handshake_persistent_base


class HandShake(handshake_persistent_base.HandShakePersistentBase):
    def __init__(self,
                 uid=None,
                 pid=None,
                 gym_id=None,
                ):
        self.uid = uid
        self.pid = pid
        self.gym_id = gym_id

    def serialize(self):
        """should return json map for this model"""
        return {
            'uid': self.uid,
            'pid': self.pid,
            'gym_id': self.gym_id,
        }

    def deserialize(self, json):
        """should return this model from dict"""
        self.uid = json["uid"]
        self.pid = json["pid"]
        self.gym_id = json["gym_id"]

    @staticmethod
    def create_model():
        return HandShake()
