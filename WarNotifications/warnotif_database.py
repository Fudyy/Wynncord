import os

from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient

load_dotenv(find_dotenv())

mongo_uri = os.environ.get('MONGO_URI')


def check_tracking(guild_name: str, mongo: MongoClient):
    collection = mongo['Wynncord']['guild_tracking']
    search = collection.find_one({'name': guild_name})

    if search:
        return True
    return False


def create_tracking(guild_name: str, channel_id: int, mongo: MongoClient):
    collection = mongo['Wynncord']['guild_tracking']
    collection.insert_one({
        'name': guild_name,
        'channels': [channel_id]
    })


def get_channels(guild_name: str):
    mongo = MongoClient(mongo_uri)
    collection = mongo['Wynncord']['guild_tracking']
    search = collection.find_one({'name': guild_name})
    result = search['channels']
    mongo.close()
    return result


def add_tracking(guild_name: str, channel_id: int):
    """
    adds a channel_id to the given guild if its being tracked.
    if not the guild is created in the database with the given channel.
    :param guild_name:
    :param channel_id:
    :return: True if its successful
    """
    mongo = MongoClient(mongo_uri)
    if not check_tracking(guild_name, mongo):
        create_tracking(guild_name, channel_id, mongo)
        mongo.close()
        return True

    collection = mongo['Wynncord']['guild_tracking']
    search = collection.find({'name': guild_name, 'channels': {"$elemMatch": {"$eq": channel_id}}})

    if len(list(search.clone())) != 0:
        mongo.close()
        return False

    collection.update_one(
        {'name': guild_name},
        {'$push': {'channels': channel_id}}
    )
    mongo.close()
    return True


def rm_tracking(guild_name: str, channel_id: int):
    mongo = MongoClient(mongo_uri)
    collection = mongo['Wynncord']['guild_tracking']
    search = collection.find_one({'name': guild_name, 'channels': {"$elemMatch": {"$eq": channel_id}}})
    if not search:
        mongo.close()
        return False

    collection.update_one({'name': guild_name},
                          {'$pull': {'channels': channel_id}})
    mongo.close()
    return True
