class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def serialize(self):
        return {
            'username': self.username,
            'password': self.password,
        }
