import json
from os import path

JSON_NAME = 'guild_tracking_data.json'


def create_json():
    if not path.isfile(JSON_NAME):
        with open(JSON_NAME, 'w') as file:
            json.dump({}, file)
            file.close()


def add_tracking(guild_name: str, channel_id: int):
    with open(JSON_NAME, 'r+') as file:
        data = json.load(file)
        if guild_name in data:
            data[guild_name]['channels'].append(channel_id)
        else:
            data[guild_name] = {
                'channels': [channel_id]
            }
        file.seek(0)
        json.dump(data, file)
        file.truncate()


def rm_tracking(guild_name: str, channel_id: int):
    with open(JSON_NAME, 'r+') as file:
        data = json.load(file)
        removed = False
        if guild_name in data:
            if channel_id in data[guild_name]['channels']:
                data[guild_name]['channels'].remove(channel_id)
                removed = True
        file.seek(0)
        json.dump(data, file)
        file.truncate()
        return removed


def check_tracking(guild_name: str):
    with open(JSON_NAME, 'r') as file:
        data = json.load(file)
        if guild_name in data:
            file.close()
            return True
        file.close()
        return False


def get_channels(guild_name: str):
    with open(JSON_NAME, 'r') as file:
        data = json.load(file)
        return data[guild_name]['channels']


if __name__ == '__main__':
    create_json()
    add_tracking('siuu', 2)
    add_tracking('siuu', 4)
    rm_tracking('siuu', 2)
