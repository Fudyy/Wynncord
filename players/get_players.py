import requests


def unpack_class_data(data):
    classes = []
    for key in data:
        classes.append(data[key])
    return classes


class PlayerClass:
    """
    Represents a player in-game class.
    """

    def __init__(self, type: str, level: int, dungeons: dict, raids: dict,
                 quests: dict, items_identified: int, mobs_killed: int, pvp: dict,
                 blocks_walked: int, logins: int, deaths: int, playtime: int,
                 gamemode: dict, skills: dict, professions: dict, discoveries: int,
                 events_won: int, pre_economy_update: bool):
        self.type = type
        self.level = level
        self.dungeons = dungeons
        self.raids = raids
        self.quests = quests
        self.items_identified = items_identified
        self.mobs_killed = mobs_killed
        self.pvp = pvp
        self.blocks_walked = blocks_walked
        self.logins = logins
        self.deaths = deaths
        self.playtime = playtime
        self.gamemode = gamemode
        self.skills = skills
        self.professions = professions
        self.discoveries = discoveries
        self.events_won = events_won
        self.pre_economy_update = pre_economy_update


class Player:
    """
    Represents a player
    """

    def __init__(self, data):
        self.username = data['username']
        self.uuid = data['uuid']
        self.rank = data['rank']
        self.meta = data['meta']
        self.characters = unpack_class_data(data['characters'])
        self.guild = data['guild']
        self.ranking = data['ranking']
        self.global_stats = data['global']


def get_players(player_name: str):
    request = requests.get(f'https://api.wynncraft.com/v2/player/{player_name}/stats').json()
    if request['code'] == 400:
        return
    data = request['data'][0]
    return Player(data)


if __name__ == '__main__':
    player = get_players('MotasKB')
    print(player.rank, player.meta['tag']['value'])
