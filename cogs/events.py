""" Handles the events Cog """
import discord
from discord.ext import commands
from loggers import logger


class Events(commands.Cog):
    """ Cog that handles events """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('Bot is ready!')
