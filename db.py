import os

from pymongo import mongo_client
from pymongo.server_api import ServerApi

uri = os.environ['DATABASE_URL']
# Create a new client and connect to the server
client = mongo_client.MongoClient(uri)
# Send a ping to confirm a successful connection
print("try ping mongo db ")

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.flask_db
# Database Collection
Users = db.Users
