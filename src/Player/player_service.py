from player_model import Player

class PlayerService:
    def __init__(self):
        pass

    def create_player_usecase(self, player_json):
        player = Player.deserialize(player_json)

    def read_player_usecase(self):
        pass

    def update_player_usecase(self):
        pass

    def delete_player_usecase(self):
        pass
