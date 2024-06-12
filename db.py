from pymongo import mongo_client
from pymongo.server_api import ServerApi
# client = mongo_client.MongoClient("localhost", 27017)

uri = "mongodb+srv://yazankaboshash:SZuSEJKcBRAk6qYK@cluster0.aksycvo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = mongo_client.MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.flask_db
# Database Collection
Users = db.Users
