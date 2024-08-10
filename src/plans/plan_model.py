from src.plans import plan_persistent_base


class Plan(plan_persistent_base.PlanPersistentBase):
    def __init__(self,
                 id=None,
                 plan_name=None,
                 price=None,
                 period=None,
                 description=None,
                 ):
        self.id = id
        self.plan_name = plan_name
        self.price = price
        self.period = period
        self.description = description

    def serialize(self):
        """should return json map for this model"""
        return {
            'id': str(self.id),
            'plan_name': self.plan_name,
            'price': self.price,
            'period': self.period,
            'description': self.description,
        }

    def serialize_to_data_base(self):
        """should return json map for this model"""
        return {
            'plan_name': self.plan_name,
            'price': self.price,
            'period': self.period,
            'description': self.description,
        }

    def deserialize(self, json):
        """should return this model from dict"""
        self.plan_name = json["plan_name"]
        self.price = json["price"]
        self.period = json["period"]
        self.description = json["description"]

    def deserialize_from_database(self, json):
        """should return this model from dict"""
        self.id = json.get("_id")
        self.plan_name = json["plan_name"]
        self.price = json["price"]
        self.period = json["period"]
        self.description = json["description"]

    @staticmethod
    def create_model():
        return Plan()
