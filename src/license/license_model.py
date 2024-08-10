
from datetime import datetime

from src.license import license_persistant_base


class License(license_persistant_base.LicensePersistentBase):
    def __init__(self,
                 _id=None,
                 gym_id=None,
                 plan_id=None,
                 price=None,
                 subscribe_date=None,
                 subscribe_end_date=None,
                 token=None,
                 product_key=None,
                 period=None
                 ):
        self.gym_id = gym_id
        self.plan_id = plan_id
        self.price = price
        self.subscribe_date = subscribe_date
        self.subscribe_end_date = subscribe_end_date
        self.token = token
        self.product_key = product_key
        self.period = period
        self._id = _id

    def serialize(self):
        """should return json map for this model"""
        return {
            '_id': str(self._id),
            'gym_id': self.gym_id,
            'plan_id': self.plan_id,
            'price': self.price,
            'subscribe_date': self.subscribe_date.strftime("%d/%m/%Y"),
            'subscribe_end_date': self.subscribe_end_date.strftime("%d/%m/%Y"),
            'token': self.token,
            'product_key': self.product_key,
            'period': self.period
        }

    def serialize_to_db(self):
        """should return json map for this model"""
        return {
            'gym_id': self.gym_id,
            'plan_id': self.plan_id,
            'price': self.price,
            'subscribe_date': self.subscribe_date.strftime("%d/%m/%Y"),
            'subscribe_end_date': self.subscribe_end_date.strftime("%d/%m/%Y"),
            'token': self.token,
            'product_key': self.product_key,
            'period': self.period
        }

    def serialize_secret(self):
        """should return json map for this model"""
        return {
            'gym_id': self.gym_id,
            'plan_id': self.plan_id,
            'price': self.price,
            'subscribe_date': self.subscribe_date.strftime("%d/%m/%Y"),
            'period': self.period
        }

    def deserialize(self, json):
        """should return this model from dict"""
        self.gym_id = json["gym_id"]
        self.plan_id = json["plan_id"]
        self.price = json["price"]
        self.subscribe_date = datetime.strptime(str(json['subscribe_date']), "%d/%m/%Y")
        self.subscribe_end_date = datetime.strptime(str(json['subscribe_end_date']), "%d/%m/%Y")
        self.token = json['token']
        self.product_key = json['product_key']
        self.period = json['period']

    def deserialize_with_id(self, json):
        """should return this model from dict"""
        self.gym_id = json["gym_id"]
        self.plan_id = json["plan_id"]
        self.price = json["price"]
        self.subscribe_date = datetime.strptime(str(json['subscribe_date']), "%d/%m/%Y")
        self.subscribe_end_date = datetime.strptime(str(json['subscribe_end_date']), "%d/%m/%Y")
        self.token = json['token']
        self.product_key = json['product_key']
        self.period = json['period']

    def deserialize_secret(self, json):
        """should return this model from dict"""
        self.gym_id = json["gym_id"]
        self.plan_id = json["plan_id"]
        self.price = json["price"]
        self.subscribe_date = datetime.strptime(str(json['subscribe_date']), "%d/%m/%Y")
        self.period = json['period']

    def deserialize_from_data_base(self, json):
        """should return this model from dict"""
        self._id = json.get("_id")
        self.gym_id = json["gym_id"]
        self.plan_id = json["plan_id"]
        self.price = json["price"]
        self.subscribe_date = datetime.strptime(str(json['subscribe_date']), "%d/%m/%Y")
        self.subscribe_end_date = datetime.strptime(str(json['subscribe_end_date']), "%d/%m/%Y")
        self.token = json['token']
        self.product_key = json['product_key']
        self.period = json['period']

    @staticmethod
    def create_model():
        return License()
