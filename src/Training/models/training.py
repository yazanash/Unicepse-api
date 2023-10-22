from src.common import models


class Training(models.PersistentBase):
    def __init__(self, id, name, images):
        super().__init__()
        self.id = id
        self.name = name
        self.images = images

    @classmethod
    def from_json(cls, json):
        return Training(json['id'], json['name'], json['images'])

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'images': self.images,
        }
