import requests as requests
from utils import logger
from datetime import datetime
from utils import convert_datetime


class Location:
    def __init__(self, startX: int, startY: int, endX: int, endY: int):
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY

    def __str__(self):
        return f"({self.startX}, {self.startY}) - ({self.endX}, {self.endY})"


class Territory:
    def __init__(self, territory: str, guild: str, guildPrefix: str, acquired: str, location: dict):
        self.name = territory
        self.guild = guild
        self.guildPrefix = guildPrefix
        self.acquired = convert_datetime(datetime.strptime(acquired, '%Y-%m-%d %H:%M:%S'))
        self.location = Location(**location)

    def __str__(self):
        return f"{self.name} ({self.guildPrefix} {self.guild}) acquired on {self.acquired} at {self.location}"


def get_territories():
    """
    Obtains all the territories from the Wynncraft API.
    Returns a list of objects with these territories.
    """
    request = requests.get(
        'https://api.wynncraft.com/public_api.php?action=territoryList').json()
    territories = request['territories']
    data = [Territory(**territories[name]) for name in territories]
    logger("Function 'get_territories' successfully called the API!.")

    return data
