from disnake.ext import commands
from disnake.interactions import ApplicationCommandInteraction as Interaction
from utils.logger import logger
from api.Player import get_player
from models.player_model import WynnPlayer


class Apitest(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot

    @commands.slash_command(name="apitest")
    async def apitest(self, interaction: Interaction, username: str):
        "Test the API"
        logger.info(f"API test requested by {interaction.author}")
        player = await get_player(username)
        if not player:
            await interaction.send(f"API test failed, player {username} not found.", ephemeral=True, delete_after=10)
            return
        await interaction.send(f"API test successful!, rank is: {player.rank}")


def setup(bot: commands.InteractionBot):
    bot.add_cog(Apitest(bot))
