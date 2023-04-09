import requests
from utils import logger, convert_datetime
from datetime import datetime


def unpack_class_data(data):
    classes = []
    for key in data:
        classes.append(data[key])
    return classes

class PlayerRanking:
    """
    Represents a player online ranking (For now the api doesn't contain any information for this data.)
    """

    def __init__(self, guild, player: dict, pvp):
        self.guild = guild
        self.player = player
        self.pvp = pvp


class PlayerGlobal:
    """
    Represents a Player cumulative class information.
    """

    def __init__(self, blocksWalked: int, itemsIdentified: int, mobsKilled: int, totalLevel: int,
                 pvp: dict, logins: int, deaths: int, discoveries: int, eventsWon: int):
        self.blocks_walked = blocksWalked
        self.items_identified = itemsIdentified
        self.mobs_killed = mobsKilled
        self.total_level = totalLevel
        self.pvp = pvp
        self.logins = logins
        self.deaths = deaths
        self.discoveries = discoveries
        self.events_won = eventsWon


class PlayerMeta:
    """
    Represents a Player metadata from the api.
    """

    def __init__(self, firstJoin: str, lastJoin: str, location: dict, playtime: int, tag: dict,
                 veteran: bool):
        self.first_join = convert_datetime(datetime.strptime(firstJoin, '%Y-%m-%dT%H:%M:%S.%fZ'))
        self.last_join = convert_datetime(datetime.strptime(lastJoin, '%Y-%m-%dT%H:%M:%S.%fZ'))
        self.is_online = location['online']
        self.online_world = location['server']
        self.playtime = playtime
        self.tag = tag
        self.veteran = veteran


class PlayerCharacter:
    """
    Represents a player in-game class, all its data is has the same model as the Wynncraft V2 API.
    """

    def __init__(self, type: str, level: int, dungeons: dict, raids: dict,
                 quests: dict, itemsIdentified: int, mobsKilled: int, pvp: dict,
                 blocksWalked: int, logins: int, deaths: int, playtime: int,
                 gamemode: dict, skills: dict, professions: dict, discoveries: int,
                 eventsWon: int, preEconomyUpdate: bool):
        self.type = type
        self.total_level = level
        self.dungeons = dungeons
        self.raids = raids
        self.quests = quests
        self.items_identified = itemsIdentified
        self.mobs_killed = mobsKilled
        self.pvp = pvp
        self.blocks_walked = blocksWalked
        self.logins = logins
        self.deaths = deaths
        self.playtime = playtime
        self.gamemode = gamemode
        self.skills = skills
        self.professions = professions
        self.discoveries = discoveries
        self.events_won = eventsWon
        self.pre_economy_update = preEconomyUpdate


class Player:
    """
    Represents a player
    """

    def __init__(self, data):
        self.username: str = data['username']
        self.uuid: int = data['uuid']
        self.rank: str = data['rank']
        self.meta = PlayerMeta(**data['meta'])
        self.characters: [] = [PlayerCharacter(**character) for character in unpack_class_data(data['characters'])]
        self.guild = data['guild']
        self.ranking = PlayerRanking(**data['ranking'])
        self.global_stats = PlayerGlobal(**data['global'])


def get_players(player_name: str):
    """
    Calls the Wynncraft V2 API for the given player name.
    Returns a Player Class.
    """
    request = requests.get(f'https://api.wynncraft.com/v2/player/{player_name}/stats').json()
    if request['code'] == 400:
        return
    data = request['data'][0]
    logger("Function 'get_players' successfully called the API!.")
    return Player(data)


if __name__ == '__main__':
    player = get_players('Fudy_')
    for character in player.characters:
        print(character.professions['combat']['level'])
