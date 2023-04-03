import discord
from discord.ext import commands
from discord import app_commands
from utils import command_logger
from guilds import get_guild
from warnotifsdata.json_data import add_tracking, rm_tracking


class Warnotifs(app_commands.Group):
    @app_commands.command(name='trackguild', description="Tracks war actvity of the guild with notifications in this channel.")
    @app_commands.describe(guild="Name of the guild to be tracked.")
    async def track_guild(self, interaction: discord.Interaction, guild: str):
        command_logger(interaction.user, '/trackguild', interaction.channel)
        data = get_guild(guild)
        if not data:
            await interaction.response.send_message(f'Guild "{guild}" not found.')
        else:
            add_tracking(data.name, interaction.channel_id)
            await interaction.response.send_message(f'"{data.name}" is now getting tracked in this channel!.')

    @app_commands.command(name='untrackguild', description="Removes a guild from getting tracked in this channel.")
    @app_commands.describe(guild="Name of the guild to be removed from tracking in this channel.")
    async def untrack_guild(self, interaction: discord.Interaction, guild: str):
        command_logger(interaction.user, '/untrackguild', interaction.channel)
        if rm_tracking(guild):
            await interaction.response.send_message(f'Guild "{guild}" has been successfully removed.')
        else:
            await interaction.response.send_message(f'Guild "{guild}" is not being tracked in this channel.')


async def setup(bot: commands.Bot):
    bot.tree.add_command(Warnotifs(
        name="war", description="Adds notifications of territory conquests."))
