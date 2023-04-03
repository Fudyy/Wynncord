import requests


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
