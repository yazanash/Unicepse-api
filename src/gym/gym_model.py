from src.gym import gym_presistent_base


class Gym(gym_presistent_base.GymPersistentBase):
    def __init__(self,
                 id=None,
                 gym_name=None,
                 owner_name=None,
                 phone_number=None,
                 telephone=None,
                 logo=None,
                 address=None
                 ):
        self.id = id
        self.gym_name = gym_name
        self.owner_name = owner_name
        self.phone_number = phone_number
        self.telephone = telephone
        self.logo = logo
        self.address = address

    def serialize(self):
        """should return json map for this model"""
        return {
            'id': str(self.id),
            'gym_name': self.gym_name,
            'owner_name': self.owner_name,
            'phone_number': self.phone_number,
            'telephone': self.telephone,
            'logo': self.logo,
            'address': self.address
        }

    def serialize_to_db(self):
        """should return json map for this model"""
        return {
            'gym_name': self.gym_name,
            'owner_name': self.owner_name,
            'phone_number': self.phone_number,
            'telephone': self.telephone,
            'logo': self.logo,
            'address': self.address
        }

    def deserialize(self, json):
        """should return this model from dict"""
        self.gym_name = json["gym_name"]
        self.owner_name = json["owner_name"]
        self.phone_number = json["phone_number"]
        self.telephone = json["telephone"]
        self.logo = json["logo"]
        self.address = json["address"]

    def deserialize_from_db(self, json):
        """should return this model from dict"""
        self.id = json.get("_id")
        self.gym_name = json["gym_name"]
        self.owner_name = json["owner_name"]
        self.phone_number = json["phone_number"]
        self.telephone = json["telephone"]
        self.logo = json["logo"]
        self.address = json["address"]

    @staticmethod
    def create_model():
        return Gym()
