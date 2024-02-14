from utils.asyncfetch import fetch_json
from models.player_model import WynnPlayer


async def get_player(username: str) -> WynnPlayer | None:
    url = f"https://api.wynncraft.com/v3/player/{username}?fullResult"
    data = await fetch_json(url)
    if data is None:
        return None
    return WynnPlayer(**data)
