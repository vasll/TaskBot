''' Handles the tasks Cog '''
from discord.ext import commands
import discord
from loggers import logger


class Tasks(commands.Cog):
    ''' Cog that contains all the commands related to tasks '''
    def __init__(self, bot):
        self.bot = bot

    @discord.command(name="ping", description="ping")
    async def ping(self, ctx):
        ''' Sends a ping response '''
        logger.info('Ping')
        await ctx.respond("Ping")
