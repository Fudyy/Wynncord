from disnake import Embed, Colour
from disnake.utils import escape_markdown, format_dt
from models.player_model import WynnPlayer


def player_profile_embed(player: WynnPlayer) -> Embed:
    """Builds an embed for the player profile."""

    rank_colour = int(player.legacy_rank_colour.main_color[1:], 16) if player.legacy_rank_colour else Colour.light_gray()

    if player.rank == "Player" and not player.support_rank:
        rank = "Player"
    elif player.rank == "Player" and player.support_rank:
        rank = player.support_rank.capitalize()
    else:
        rank = player.rank.capitalize()

    # Main embed information
    embed = Embed(
        title=escape_markdown(player.username),
        url=f"https://wynncraft.com/stats/player/{player.username}",
        color=rank_colour,
        description=f"**Rank:** {rank}\n"
    )

    embed.set_author(
        name="WynnCraft profile for:",
        icon_url=f"https://cdn.wynncraft.com/nextgen/wynncraft_icon.png"
    )

    embed.set_thumbnail(url=f"https://mc-heads.net/head/{player.username}/left")

    # Online fields
    if player.online:
        embed.add_field(name="Status:", value=f"🟢 Online", inline=True)
        embed.add_field(name="", value="", inline=True)
        embed.add_field(name="Server:", value=f"{player.server}", inline=True)
    else:
        embed.add_field(name="Status:", value="🔴 Offline", inline=True)
        embed.add_field(name="", value="", inline=True)
        embed.add_field(name="Last online:", value=f"{format_dt(player.last_join, 'R')}", inline=True)

    # Guild fields (if exists)
    if player.guild:
        embed.add_field(name="Guild:", value=f"{player.guild.name}", inline=True)
        embed.add_field(name="", value="", inline=True)
        embed.add_field(name="Guild rank:", value=f"{player.guild.rank.capitalize()}", inline=True)

    # Level and first join fields
    embed.add_field(name="Total level:", value=f"{player.global_data.total_level}", inline=True)
    embed.add_field(name="", value="            ", inline=True)
    embed.add_field(name="First join:", value=f"{format_dt(player.first_join, 'f')}", inline=True)

    return embed
