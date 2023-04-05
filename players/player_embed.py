from players import get_players, Player
from discord import Embed

rank_color = {
    'Player': 0xc9c9c9,
    'VIP': 0x25a22d,
    'VIP+': 0x0098a3,
    'HERO': 0xc800d6,
    'CHAMPION': 0xfbff05,
    'Media': 0xff00f7,
    'Moderator:': 0xeb9500,
    'Game Master': 0x00fbff,
    'CMD': 0x00fbff,
    'Item': 0x00fbff,
    'Builder': 0x00fbff,
    'Hybrid': 0x00fbff,
    'Music': 0x00fbff,
    'WebDev': 0xff0000,
    'Administrator': 0xff0000
}
def embed_constructor(player: Player):
    embed = Embed(color=0x933434)
    embed.set_author(name=f"{player.username}", url=f"https://wynncraft.com/stats/player/{player.username}",
                     icon_url="https://cdn.wynncraft.com/nextgen/wynncraft_icon.png")
    embed.set_thumbnail(url=f"https://mc-heads.net/head/{player.username}/left")

    return embed