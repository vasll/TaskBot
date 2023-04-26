""" Runs the TaskBot with a token from the config.py file """
import config
from loggers import logger
import db.schemas
from taskbot import TaskBot


# Create the db with tables if they don't exist
db.schemas.create_all_tables()

# Run the bot
logger.info('Starting TaskBot')
bot = TaskBot()
bot.run(config.bot['token'])
