from disnake.ext import commands
from disnake.interactions import ApplicationCommandInteraction as Interaction
from utils.logger import logger
from api.Player import get_player
from messages.embeds.player_profile import player_profile_embed


class Player(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot

    @commands.slash_command(name="player")
    async def player(self, interaction: Interaction):
        pass

    @player.sub_command(name="profile", description="Get a player's profile.")
    async def profile(self, interaction: Interaction, username: str = commands.Param(description="The player to search "
                                                                                                 "for.")):
        logger.info(f"Player information requested on: {interaction.guild_id} by {interaction.author} for {username}.")
        player = await get_player(username)
        if not player:
            await interaction.send(f"Player {username} was not found.", ephemeral=True, delete_after=10)
            return
        await interaction.send(embed=player_profile_embed(player))


def setup(bot: commands.InteractionBot):
    bot.add_cog(Player(bot))
