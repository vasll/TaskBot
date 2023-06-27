""" Contains the TaskBot class """
import discord
import config
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
    

# Utils
def restore_commands(bot = discord.Bot()):
    """  
    When subclassing discord.Bot() if new commands are added to a cog they don't get registered. 
    The temporary workaround is to create a "raw" Bot() and add the cogs to it and run it, then the commands get registered 
    """
    logger.info("Restoring bot commands...")
    bot.add_cog(tasks.Tasks(bot))
    bot.add_cog(setup.Setup(bot))
    bot.add_cog(loops.Loops(bot))

    @bot.event
    async def on_ready():
        print("Commands restored. Exiting")
        exit(0)

    bot.run(config.bot['token'])
