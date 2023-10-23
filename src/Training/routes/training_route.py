from flask import Blueprint

trainingBlueprint = Blueprint("training", __name__)


@trainingBlueprint.route('/training/<int:player_id>/<int:ids>', methods=["GET"])
def training_handler(player_id, ids):
    return f"<h1>YOU ENTERED player_id: {player_id, ids}</h1>"
