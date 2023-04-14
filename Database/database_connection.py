from pymongo import MongoClient
import os
def get_database():
    database_uri = os.environ.get('MONGO_URI')
    client = MongoClient(database_uri)

    return client['Wynncord']