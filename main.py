""" Runs the bot with the token from a config.py file """
import discord
from discord.ext import commands
from cogs import tasks, events, setup
import config
from loggers import logger
from schemas import create_all_tables


logger.info('Starting bot')
create_all_tables()

# Variables
intents = discord.Intents(members=True, presences=True, messages=True, guilds=True, bans=True)
bot = commands.Bot(intents=intents)

# Cogs
bot.add_cog(tasks.Tasks(bot))
bot.add_cog(setup.Setup(bot))
bot.add_cog(events.Events(bot))


# Run the bot
bot.run(config.bot['token'])
