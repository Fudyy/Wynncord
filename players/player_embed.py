from discord import Embed
from discord.utils import format_dt, escape_markdown
from players import Player

rank_color = {
    'Player': 0xc9c9c9,
    'VIP': 0x25a22d,
    'VIP+': 0x0098a3,
    'HERO': 0xc800d6,
    'CHAMPION': 0xfbff05,
    'Media': 0xff00f7,
    'Moderator': 0xff4d00,
    'Game Master': 0x00fbff,
    'CMD': 0x00fbff,
    'Item': 0x00fbff,
    'Builder': 0x00fbff,
    'Hybrid': 0x00fbff,
    'Music': 0x00fbff,
    'WebDev': 0xff0000,
    'Administrator': 0xff0000
}


def get_rank_info(player: Player):
    """Gets the rank and the color of it in a simple way"""
    if player.rank == 'Player' and player.meta.tag['value']:
        rank = player.meta.tag['value']
    elif player.rank == 'Player' and not player.meta.tag['value']:
        rank = 'Player'
    else:
        rank = player.rank

    color = rank_color[rank]

    return rank, color


def embed_constructor(player: Player):
    rank, color = get_rank_info(player)

    embed = Embed(title=f"{escape_markdown(player.username)}", color=color, url=f"https://wynncraft.com/stats/player/{player.username}")
    embed.set_thumbnail(url=f"https://mc-heads.net/head/{player.username}/left")
    embed.set_author(name="Wynncraft profile for:", icon_url="https://cdn.wynncraft.com/nextgen/wynncraft_icon.png")

    # Check if the player is online
    if not player.meta.is_online:
        embed.add_field(name="Status:", value="🔴 Offline", inline=True)
        embed.add_field(name="Last seen:", value=format_dt(player.meta.last_join, 'R'), inline=True)
    else:
        embed.add_field(name="Status:", value="🟢 Online", inline=True)
        embed.add_field(name="Server:", value=player.meta.online_world)

    return embed
