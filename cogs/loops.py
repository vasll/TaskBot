""" Contains all the looping and timed tasks -> [https://docs.pycord.dev/en/stable/ext/tasks/index.html] """
import discord
import db.gdrive_utils as gdrive
import config
from discord import Activity, ActivityType
from discord.ext import commands, tasks
from db import queries
from loggers import logger
from datetime import datetime


class Loops(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.presence_updater.start()
        self.backup_db.start()
        self.has_first_backup_been_ignored = False

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

    @tasks.loop(hours=config.backups_frequency_hours)
    async def backup_db(self):
        """ Uploads a backup of the database to a google drive service account """
        if config.enable_backups is False:
            return

        if self.has_first_backup_been_ignored is False:     # Ignore first backup on startup
            self.has_first_backup_been_ignored = True
            return

        logger.info("Peforming backup of './db/taskbot.db'...")
        try:
            upload_file_name = f"taskbot_{datetime.now().strftime('%d-%m-%Y_%H:%M')}.db"
            uploaded_file = gdrive.upload_file_to_gdrive(
                "./db/taskbot.db", upload_file_name, config.backups_folder_id
            )
            logger.info(f"Uploaded database backup to google drive as '{uploaded_file['name']}'")
        except Exception as e:
            logger.error(f"Couldn't upload database backup to google drive. Exception: {e}")

    @presence_updater.before_loop
    @backup_db.before_loop
    async def wait_for_bot_ready(self):
        await self.bot.wait_until_ready()
