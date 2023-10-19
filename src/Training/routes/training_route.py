from flask import Blueprint

trainingBlueprint = Blueprint("training", __name__)


@trainingBlueprint.route('/training', methods=["GET"])
def traiing_handler():
    return "blah"
