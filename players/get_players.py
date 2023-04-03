import requests
from datetime import datetime


class PlayerClass:
    def __init__(self, type, level, dungeons, raids, quests):
        self.type = type
        self.level = level
        self.dungeons_completed = dungeons["completed"]
        self.dungeons_list = dungeons["list"]
        self.raids_completed = raids["completed"]
        self.raids_list = raids["list"]
        self.quests_completed = quests["completed"]
        self.quests_list = quests["list"]


class PlayerMeta:
    def __init__(self, first_join: str, last_join: str, location: dict, playtime: int, tag: dict, veteran: bool):
        self.first_join = datetime.strptime(first_join, "%Y-%m-%dT%H:%M:%S.%fZ")
        self.last_join = datetime.strptime(last_join, "%Y-%m-%dT%H:%M:%S.%fZ")
        self.location = location
        self.playtime = playtime
        self.tag = tag
        self.veteran = veteran


class Player:
    def __init__(self, data):
        self.username = data['username']
        self.uuid = data['uuid']
        self.rank = data['rank']
        self.meta = data['meta']
        self.characters = data['characters']
        self.guild = data['guild']
        self.ranking = data['ranking']
        self.global_stats = data['global']


def get_players(player_name: str):
    request = requests.get(f'https://api.wynncraft.com/v2/player/{player_name}/stats').json()
    if request['code'] == 400:
        return
    data = request['data'][0]
    return Player(data)
