from pymongo import mongo_client

client = mongo_client.MongoClient("localhost", 27017)
db = client.flask_db

