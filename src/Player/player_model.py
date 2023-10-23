from src.common import models


class Player(models.PersistentBase):
    def __init__(self, id, name, width, height):
        super().__init__()
        self.id = id
        self.name = name
        self.width = width
        self. height = height

    @staticmethod
    def deserialize(json):
        """Deserializes a player from dict {json}"""
        return Player(
            json['id'],
            json['name'],
            json['width'],
            json['height']
        )

    def serialize(self):
        """Serializes player to dict {json}"""
        return {
            'id': self.id,
            'name': self.name,
            'width': self.width,
            'height': self.height,
        }
