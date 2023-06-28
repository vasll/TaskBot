""" Contains all the looping and timed tasks -> [https://docs.pycord.dev/en/stable/ext/tasks/index.html] """
import discord
from discord import Activity, ActivityType
from discord.ext import commands, tasks
from db import queries
from loggers import logger


class Loops(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.presence_updater.start()

    @tasks.loop(minutes=5.0)
    async def presence_updater(self):
        """ Updates the bot's presence with the total task count from the db """
        try:
            task_count = await queries.get_task_count()
            if task_count is None:
                return
        except Exception as e:
            logger.error(f"Error in tasks.loop while fetching task count: {e}")

        activity = Activity(type=ActivityType.watching, name=f"{task_count} tasks")
        await self.bot.change_presence(activity=activity)

    @presence_updater.before_loop
    async def before_presence_updater(self):
        await self.bot.wait_until_ready()
