""" Handles the tasks Cog """
from discord.ext import commands
import discord
from discord.commands.context import ApplicationContext
from loggers import logger


class Tasks(commands.Cog):
    """ Cog that contains all the commands related to tasks """

    def __init__(self, bot):
        self.bot = bot

    @discord.command(name="ping", description="ping")
    async def ping(self, ctx: ApplicationContext):
        # TODO remove this later
        logger.debug('Ping')
        await ctx.respond("Ping")
