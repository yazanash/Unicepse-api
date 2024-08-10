from src.offer import offer_persistent_base


class Offer(offer_persistent_base.OfferPersistentBase):
    def __init__(self,
                 id=None,
                 offer_name=None,
                 offer_percent=None,
                 period=None,
                 description=None,
                 ):
        self.id = id
        self.offer_name = offer_name
        self.offer_percent = offer_percent
        self.period = period
        self.description = description

    def serialize(self):
        """should return json map for this model"""
        return {
            'id': str(self.id),
            'offer_name': self.offer_name,
            'offer_percent': self.offer_percent,
            'period': self.period,
            'description': self.description,
        }

    def serialize_to_data_base(self):
        """should return json map for this model"""
        return {
            'offer_name': self.offer_name,
            'offer_percent': self.offer_percent,
            'period': self.period,
            'description': self.description,
        }

    def deserialize(self, json):
        """should return this model from dict"""
        self.offer_name = json["offer_name"]
        self.offer_percent = json["offer_percent"]
        self.period = json["period"]
        self.description = json["description"]

    def deserialize_from_database(self, json):
        """should return this model from dict"""
        self.id = json.get("_id")
        self.offer_name = json["offer_name"]
        self.offer_percent = json["offer_percent"]
        self.period = json["period"]
        self.description = json["description"]

    @staticmethod
    def create_model():
        return Offer()
