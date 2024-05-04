from flask import Blueprint, request
from gridfs import GridFS
from db import db
trainingBlueprint = Blueprint("training", __name__)

