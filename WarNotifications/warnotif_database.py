from os import environ
from pymongo import MongoClient

database_uri = environ.get('MONGO_URI')
client = MongoClient(database_uri)['Wynncord']



def check_tracking(guild_name: str):
    """
    Checks if the given guild is in the database
    :param guild_name:
    :return: True if its found.
    """
    collection = client['guild_tracking']
    search = collection.find_one({'name': guild_name})

    if search:
        return True
    return False


def create_tracking(guild_name: str, channel_id: int):
    collection = client['guild_tracking']
    collection.insert_one({
        'name': guild_name,
        'channels': [channel_id]
    })

def get_channels(guild_name: str):
    collection = client['guild_tracking']
    search = collection.find_one({'name': guild_name})
    return search['channels']


def add_tracking(guild_name: str, channel_id: int):
    """
    adds a channel_id to the given guild if its being tracked.
    if not the guild is created in the database with the given channel.
    :param guild_name:
    :param channel_id:
    :return: True if its successful
    """
    if not check_tracking(guild_name):
        create_tracking(guild_name, channel_id)
        return True

    collection = client['guild_tracking']
    search = collection.find({'name': guild_name, 'channels': {"$elemMatch": {"$eq": channel_id}}})

    if len(list(search.clone())) != 0:
        return False

    collection.update_one(
        {'name': guild_name},
        {'$push': {'channels': channel_id}}
    )
    return True


def rm_tracking(guild_name: str, channel_id: int):
    collection = client['guild_tracking']
    search = collection.find_one({'name': guild_name, 'channels': {"$elemMatch": {"$eq": channel_id}}})
    if not search:
        return False

    collection.update_one({'name': guild_name},
                          {'$pull': {'channels': channel_id}})
    return True
