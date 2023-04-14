import os
from typing import List

from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient

from MessageEmbeds.territory_embed import embed_territory
from WarNotifications.warnotif_database import check_tracking, get_channels, rm_tracking
from WynnAPI.territories import get_territories, Territory

load_dotenv(find_dotenv())
old_data = []
mongo_uri = os.environ.get('MONGO_URI')


def territory_count(data: List[Territory]):
    """
    Counts the territories held by each guild in the given data
    :param data: list of Territories
    :return: dictionary of the guilds with their respective territory count.
    """
    territory_count = {}

    for territory in data:
        if territory.guild not in territory_count:
            territory_count[territory.guild] = 1
        else:
            territory_count[territory.guild] += 1

    return territory_count


async def send_embeds(bot: commands.Bot,
                      new_territory: Territory, old_territory: Territory,
                      new_territory_count: int, old_territory_count: int,
                      channels, lost: bool):
    for channel in channels:
        try:
            embed = embed_territory(
                new_territory,
                old_territory,
                new_territory_count,
                old_territory_count,
                lost
            )
            await bot.get_channel(channel).send(embed=embed)
        except:
            await rm_tracking(new_territory.guild, channel)


async def war_notification_loop(bot: commands.Bot):
    """
    Gets the territory list from the api and compares it with the last one called.
    Then it send a notification to the saved channels with the respective tracked guild.
    """

    global old_data
    data = get_territories()

    # First call doesn't have changes, so it saves the data.
    if not old_data:
        old_data = {t.name: t for t in data}
        return

    # Counts the number of territories of each guild in the data for later use
    counted_territories = territory_count(data)

    mongo = MongoClient(mongo_uri)

    # Comparison of the new data with the saved data
    for new_territory in data:

        old_territory: Territory = old_data[new_territory.name]

        if old_territory == new_territory:
            continue

        captured_is_tracked = check_tracking(new_territory.guild, mongo)
        lost_is_tracked = check_tracking(old_territory.guild, mongo)
        if not captured_is_tracked or not lost_is_tracked:
            continue

        # If the two guilds are being tracked in the same channel the capture has priority over the loss.
        if captured_is_tracked:
            lost = False
            channels = get_channels(new_territory.guild)
        else:
            lost = True
            channels = get_channels(old_territory.guild)

        # if the old territory is not in the territory count the guild doesn't have any territories held
        if old_territory not in counted_territories:
            counted_territories[old_territory.guild] = 0

        await send_embeds(bot, new_territory, old_territory,
                          counted_territories[new_territory.guild],
                          counted_territories[old_territory.guild],
                          channels, lost)
