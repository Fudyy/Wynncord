import discord
from discord.ext import commands, tasks

from utils import logger
from commandHandler import command_handler
from warnotifsdata.data_comparision import data_comparision

# .env setup
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Client configuration
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)


@bot.event
async def on_ready():
    logger(f'Bot working in client: {bot.user}')
    await command_handler(bot)
    warnotif.start()


@tasks.loop(seconds=30)
async def warnotif():
    await data_comparision(bot)


if __name__ == '__main__':
    bot.run(os.environ.get('TOKEN'))
