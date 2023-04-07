import discord
from discord.ext import commands
from discord import app_commands
from players import get_players, player_embed
from utils import command_logger

class Players(app_commands.Group):

    @app_commands.command(name='profile', description='Checks the Wynn profile of the given player')
    @app_commands.describe(player='Player to search')
    async def stats(self, interaction: discord.Interaction, player: str):
        command_logger(interaction.user.name, 'player stats', interaction.channel_id.__str__())
        player = get_players(player)
        if not player:
            await interaction.response.send_message(f'no')
        else:
            await interaction.response.send_message(embed=player_embed.profile_embed_constructor(player))


async def setup(bot: commands.Bot):
    bot.tree.add_command(Players(name='player'))