from discord import Embed
from discord.utils import format_dt, escape_markdown
from players import Player

rank_color = {
    'Player': 0xc9c9c9,  # Gray
    'VIP': 0x25a22d,  # Green
    'VIP+': 0x00fbff,  # Aqua
    'HERO': 0x9000ff,  # Purple
    'CHAMPION': 0xfbff05,  # Yellow
    'Media': 0xff00ff,  # Pink
    'Moderator': 0xff4d00,  # Orange
    'Game Master': 0x0098a3,  # Cyan
    'CMD': 0x0098a3,  # Cyan
    'Item': 0x0098a3,  # Cyan
    'Builder': 0x0098a3,  # Cyan
    'Hybrid': 0x0098a3,  # Cyan
    'Music': 0x0098a3,  # Cyan
    'WebDev': 0xff0000,  # Red
    'Administrator': 0xff0000 # Red
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


def profile_embed_constructor(player: Player):
    rank, color = get_rank_info(player)

    embed = Embed(title=f"{escape_markdown(player.username)}", color=color,
                  url=f"https://wynncraft.com/stats/player/{player.username}")
    embed.set_thumbnail(url=f"https://mc-heads.net/head/{player.username}/left")
    embed.set_author(name="Wynncraft profile for:", icon_url="https://cdn.wynncraft.com/nextgen/wynncraft_icon.png")

    # Check if the player is online
    if not player.meta.is_online:
        embed.add_field(name="Status:", value="🔴 Offline", inline=True)
        embed.add_field(name="", value="", inline=True)
        embed.add_field(name="Last seen:", value=format_dt(player.meta.last_join, 'R'), inline=True)
    else:
        embed.add_field(name="Status:", value="🟢 Online", inline=True)
        embed.add_field(name="", value="", inline=True)
        embed.add_field(name="Server:", value=player.meta.online_world)

    embed.add_field(name="", value="", inline=True)
    embed.add_field(name="", value="====✴️====", inline=True)
    embed.add_field(name="", value="", inline=True)

    embed.add_field(name="Rank:", value=f"{rank.capitalize()}", inline=False)

    # Check if the player has a guild
    if player.guild['name']:
        embed.add_field(name="Guild:", value=f"{player.guild['name']}", inline=True)
        embed.add_field(name="", value="", inline=True)
        embed.add_field(name="Guild rank:", value=f"{player.guild['rank'].capitalize()}", inline=True)


    embed.add_field(name="Total level:", value=f"{player.global_stats.total_level['combined']}", inline=True)
    embed.add_field(name="", value="", inline=True)
    embed.add_field(name="First join:", value=f"{format_dt(player.meta.first_join, 'f')}", inline=True)

    return embed
