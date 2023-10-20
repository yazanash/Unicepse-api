class Player:
    def __init__(self, id, name, width, height):
        self.id = id
        self.name = name
        self.width = width
        self. height = height

    @classmethod
    def from_json(cls, json):
        return Player(json['id'], json['name'], json['width'], json['height'])

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'width': self.width,
            'height': self.height,
        }
