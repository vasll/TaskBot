""" Runs the TaskBot with a token from the config.py file """
import config
from loggers import logger
from taskbot import TaskBot


# Run the bot
logger.info('Starting TaskBot')
bot = TaskBot()
bot.run(config.bot['token'])
