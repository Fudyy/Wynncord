from typing import List

from discord.ext import commands

from territories import get_territories
from territories.get_territories import Territory
from warnotifsdata.json_data import create_json, check_tracking, get_channels, rm_tracking
from warnotifsdata.territory_embed import embed_territory

old_data = []


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
