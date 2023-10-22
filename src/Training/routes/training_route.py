from flask import Blueprint

trainingBlueprint = Blueprint("training", __name__)


@trainingBlueprint.route('/training', methods=["GET"])
def training_handler():
    return "blah"
