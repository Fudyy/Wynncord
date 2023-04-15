import discord
from discord.ext import commands

from utils import logger
from commandHandler import command_handler

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


if __name__ == '__main__':
    bot.run(os.environ.get('TOKEN'))
