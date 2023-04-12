from datetime import datetime
from discord import Embed
from discord.utils import format_dt
from WynnAPI.territories import Location, Territory


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

    embed = Embed(title=f"Captured by: {new_territory.guild}",
                          url=f"https://www.wynncraft.com/stats/guild/{new_territory.guild.replace(' ', '%20')}",
                          color=color)
    embed.set_author(name=f'{new_territory.name}',
                     url=f"https://map.wynncraft.com/#/{coordinateX}/64/{coordinateY}/-1/wynn-main/Wynncraft")
    embed.set_thumbnail(url="https://cdn.wynncraft.com/nextgen/wynncraft_icon.png")
    embed.add_field(name="Captured at:", value=format_dt(new_territory.acquired, style='R'),
                    inline=True)
    embed.add_field(name=f"{new_territory.guild} is now holding:", value=f"{new_territory_count} Territories",
                    inline=True)
    embed.add_field(name="Former owner:", value=f'{old_territory.guild}', inline=False)
    embed.add_field(name="Time captured:", value=get_time_captured(new_territory.acquired, old_territory.acquired),
                    inline=True)
    embed.add_field(name=f"{old_territory.guild} is now holding:", value=f"{old_territory_count} Territories",
                    inline=True)

    return embed