import datetime
from typing import List

import requests
from utils import logger


class Member:
    def __init__(self, name: str, uuid: str, rank: str, contributed: int, joined: datetime, joinedFriendly: str):
        self.name = name
        self.uuid = uuid
        self.rank = rank
        self.contributed = contributed
        self.joined = joined
        self.joinedFriendly = joinedFriendly


class Guild:
    def __init__(self, name: str, prefix: str, members: List[dict], xp: int, level: int, created: datetime,
                 createdFriendly: str, territories: int, request: dict ,banner: dict = {}):
        self.name = name
        self.prefix = prefix
        self.members = [Member(**member) for member in members]
        self.xp = xp
        self.level = level
        self.created = created
        self.createdFriendly = createdFriendly
        self.territories = territories
        self.banner = banner
        self.request = request


def get_guild(name: str):
    request = requests.get(f"https://api.wynncraft.com/public_api.php?action=guildStats&command={name.replace(' ', '%20')}").json()
    logger("'Function 'get_guild' successfully called the API!.")
    try:
        return Guild(**request)
    except:
        return