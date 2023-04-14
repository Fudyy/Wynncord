from os import environ

from pymongo import MongoClient

database_uri = environ.get('MONGO_URI')



def check_tracking(guild_name: str):
    """
    Checks if the given guild is in the database
    :param guild_name:
    :return: True if its found.
    """
    client = MongoClient(database_uri)
    collection = client['Wynncord']['guild_tracking']
    search = collection.find_one({'name': guild_name})

    if search:
        client.close()
        return True
    client.close()
    return False


def create_tracking(guild_name: str, channel_id: int):
    client = MongoClient(database_uri)
    collection = client['Wynncord']['guild_tracking']
    collection.insert_one({
        'name': guild_name,
        'channels': [channel_id]
    })
    client.close()


def get_channels(guild_name: str):
    client = MongoClient(database_uri)
    collection = client['Wynncord']['guild_tracking']
    search = collection.find_one({'name': guild_name})
    result = search['channels']
    client.close()
    return result


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

    client = MongoClient(database_uri)
    collection = client['Wynncord']['guild_tracking']
    search = collection.find({'name': guild_name, 'channels': {"$elemMatch": {"$eq": channel_id}}})

    if len(list(search.clone())) != 0:
        client.close()
        return False

    collection.update_one(
        {'name': guild_name},
        {'$push': {'channels': channel_id}}
    )
    client.close()
    return True


def rm_tracking(guild_name: str, channel_id: int):
    client = MongoClient(database_uri)
    collection = client['Wynncord']['guild_tracking']
    search = collection.find_one({'name': guild_name, 'channels': {"$elemMatch": {"$eq": channel_id}}})
    if not search:
        client.close()
        return False

    collection.update_one({'name': guild_name},
                          {'$pull': {'channels': channel_id}})
    client.close()
    return True
