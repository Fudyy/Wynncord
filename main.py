import disnake
from disnake.ext import commands
import os
from dotenv import load_dotenv
from platform import python_version
from utils.logger import logger
from sys import exit

load_dotenv()

token = os.getenv("TOKEN")

if token is None:
    logger.error("No token provided on environment variables.")
    exit()

bot = commands.InteractionBot(owner_id=237719849541959681, test_guilds=[1160695207101214853], activity=
disnake.Activity(type=disnake.ActivityType.playing, name="Fruma waiting room!"))


@bot.event
async def on_ready():
    logger.info("=" * 30)
    logger.info(f"Bot is running on client: {bot.user}")
    logger.info(f"Client ID: {bot.user.id}")
    logger.info(f"Python version: {python_version()}")
    logger.info(f"Disnake package version: {disnake.__version__}")
    logger.info("=" * 30)


def load_commands():
    try:
        commands_dir = os.listdir("commands")
        logger.info("Started loading commands")
        for file in commands_dir:
            if file.endswith(".py"):
                logger.info(f"Loading command: {file[:-3]}")
                bot.load_extension(f"commands.{file[:-3]}")
                logger.info(f"Successfully loaded command: {file[:-3]}")
    except FileNotFoundError as err:
        logger.error(f"There was an error loading the commands: {err}")
        exit()


if __name__ == '__main__':
    load_commands()
    bot.run(token)
