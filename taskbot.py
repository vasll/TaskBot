""" Contains the TaskBot class """
import discord
from discord.ext.commands import Bot
from cogs import tasks, setup
from loggers import logger
from views.task_view import TaskView
from views.role_view import RoleView


class TaskBot(Bot):
    intents = discord.Intents(members=True, presences=True, messages=True, guilds=True, bans=True, message_content=True)

    def __init__(self):
        # Initialize bot
        super().__init__(intents=self.intents)

        # Add cogs to bot
        self.add_cog(tasks.Tasks(self))
        self.add_cog(setup.Setup(self))
    

    async def on_ready(self):
        # Add views to bot
        self.add_view(TaskView())
        self.add_view(RoleView())

        logger.info('Bot is ready!')
    
