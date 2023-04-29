""" Contains the TaskBot class """
import discord
from discord.ext.commands import Bot
from loggers import logger
from db import queries, database
from cogs import tasks, setup, loops
from views.task_view import TaskView
from views.role_view import RoleView


class TaskBot(Bot):
    intents = discord.Intents(
        members=True, messages=True, guilds=True, bans=True, message_content=True
    )

    def __init__(self):
        super().__init__(intents=self.intents)
        self.persistent_views_added = False
        self.add_cog(tasks.Tasks(self))
        self.add_cog(setup.Setup(self))
        self.add_cog(loops.Loops(self))
    
    async def on_connect(self):
        await queries.create_all_tables(database.engine)

    async def on_ready(self):
        # Add views to bot to make them persistent
        if not self.persistent_views_added:
            self.add_view(TaskView())
            self.add_view(RoleView())
            self.persistent_views_added = True
        logger.info('Bot is ready!')
    
