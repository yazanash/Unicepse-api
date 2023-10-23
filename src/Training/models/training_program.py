from src.common import models


class TrainingProgram(models.PersistentBase):
    def __init__(self, id, name, training_list, provider):
        super().__init__()
        self.id = id
        self.name = name
        self.training_list = training_list
        self.provider = provider

    @staticmethod
    def deserialize(json):
        """Deserializes TrProg from dict {json}"""
        return TrainingProgram(
            json['id'],
            json['name'],
            json['training_list'],
            json['provider'],
        )

    def serialize(self):
        """serializes TrProg to dict {json}"""
        return {
            'id': self.id,
            'name': self.name,
            'training_list': self.training_list,
            'provider': self.provider,
        }
