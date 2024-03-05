from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def connect_to_mongo():
    username = "fer"
    password = "contra12"
    client =f"mongodb+srv://{username}:{password}@cluster0.lbk9v9l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(client, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
        print('Connected to MongoDB')
        return client
    except Exception as e:
        print(e)
        return False
    