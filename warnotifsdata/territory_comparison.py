import discord
from discord.ext import commands
from datetime import datetime
from typing import List
from territories import get_territories
from territories.get_territories import Territory, Location
from warnotifsdata.json_data import create_json, check_tracking, get_channels, rm_tracking

old_data = []


def get_web_coordinates(location: Location):
    """
    Gets the center coordinates of the given Location.
    """
    coordinateX = (location.startX + location.endX) / 2
    coordinateY = (location.startY + location.endY) / 2

    return coordinateX, coordinateY


def get_time_captured(newdate: datetime, olddate: datetime):
    time_captured = newdate - olddate
    # Convert the time difference into days, hours, minutes, and seconds
    days = time_captured.days
    hours, seconds = divmod(time_captured.seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    # Create a list with the components we want to include in the final result
    components = [("days", days), ("hours", hours), ("minutes", minutes), ("seconds", seconds)]

    # Create a list with the components that have a non-zero value
    non_zero_components = [f"{value} {name}" for name, value in components if value != 0]

    # Print the result in the format "days:hours:minutes:seconds"
    result = " ".join(non_zero_components)

    return result


def embed_territory(new_territory: Territory, old_territory: Territory, new_territory_count: int,
                    old_territory_count: int, loss=False):
    """
    Creates the embed message for the notification.

    loss = If the message is green/red.
    """
    coordinateX, coordinateY = get_web_coordinates(new_territory.location)

    color = 0x0fb31a
    if loss:
        color = 0xf21c1c

    embed = discord.Embed(title=f"Captured by: {new_territory.guild}",
                          url=f"https://www.wynncraft.com/stats/guild/{new_territory.guild.replace(' ', '%20')}",
                          color=color)
    embed.set_author(name=f'{new_territory.territory}',
                     url=f"https://map.wynncraft.com/#/{coordinateX}/64/{coordinateY}/-1/wynn-main/Wynncraft")
    embed.set_thumbnail(url="https://cdn.wynncraft.com/nextgen/wynncraft_icon.png")
    embed.add_field(name="Captured at:", value=discord.utils.format_dt(new_territory.acquired, style='R'),
                    inline=True)
    embed.add_field(name=f"{new_territory.guild} is now holding:", value=f"{new_territory_count} Territories",
                    inline=True)
    embed.add_field(name="Former owner:", value=f'{old_territory.guild}', inline=False)
    embed.add_field(name="Time captured:", value=get_time_captured(new_territory.acquired, old_territory.acquired),
                    inline=True)
    embed.add_field(name=f"{old_territory.guild} is now holding:", value=f"{old_territory_count} Territories",
                    inline=True)

    return embed


def territory_count(data: List[Territory]):
    territory_count = {}

    # Counts the territories held by each guild in the given data
    for territory in data:
        if territory.guild not in territory_count:
            territory_count[territory.guild] = 1
        else:
            territory_count[territory.guild] += 1

    return territory_count


async def data_comparison(bot: commands.Bot):
    """
    Gets the territory list from the api and compares it with the last one called.
    Then it send a notification to the saved channels with the respective tracked guild.
    """

    # Json with all the data from tracked guilds and channels to send notifications.
    create_json()

    # First call doesn't have changes, so it saves it.
    global old_data
    data = get_territories()
    if not old_data:
        old_data = {t.territory: t for t in data}

    counted_territories = territory_count(data)

    # Compare if there is a change from the old data with the new one.
    for territory in data:

        old_territory = old_data.get(territory.territory)
        if old_territory and territory.guild != old_territory.guild:

            # Checks if the change correspond to a tracked guild
            territory_tracked = check_tracking(territory.guild)
            if territory_tracked or check_tracking(old_territory.guild):

                # if the old territory is not in the territory count the guild doesn't have any territories held
                if old_territory.guild not in counted_territories:
                    counted_territories[old_territory.guild] = 0

                # Checks if is a lost or won territory
                if not territory_tracked:
                    lost = True
                    channels = get_channels(old_territory.guild)
                else:
                    lost = False
                    channels = get_channels(territory.guild)

                for channel_id in channels:
                    try:
                        embed = embed_territory(territory,
                                                old_territory,
                                                counted_territories[territory.guild],
                                                counted_territories[old_territory.guild],
                                                lost)
                        await bot.get_channel(channel_id).send(embed=embed)
                    except:
                        rm_tracking(territory.guild, channel_id)

            old_data[territory.territory] = territory
