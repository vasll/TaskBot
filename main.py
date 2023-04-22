""" Runs the TaskBot with a token from the config.py file """
import config
from loggers import logger
from schemas import create_all_tables
from task_bot import TaskBot


# Run the bot
create_all_tables()  # This is optional
logger.info('Starting TaskBot')
bot = TaskBot()
bot.run(config.bot['token'])
