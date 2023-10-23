from src.common import models


class Training(models.PersistentBase):
    def __init__(self, id, name, rounds, image_url):
        super().__init__()
        self.id = id
        self.name = name
        self.rounds = rounds
        self.image_url = image_url

    @staticmethod
    def deserialize(json):
        """Deserializes Training from dict {json}"""
        return Training(
            json['id'],
            json['name'],
            json['rounds'],
            json['image_url'],
        )

    def serialize(self):
        """Serializes Training to dict {json}"""
        return {
            'id': self.id,
            'name': self.name,
            'rounds': self.rounds,
            'image_url': self.image_url,
        }
