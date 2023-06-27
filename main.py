""" Runs the TaskBot with a token from the config.py file """
import config, discord
from loggers import logger
from taskbot import TaskBot, restore_commands
from argparse import ArgumentParser, BooleanOptionalAction


# Load args
argparser = ArgumentParser("python main.py")
argparser.add_argument("--restore-commands", help="Forces the bot commands to get registered", action=BooleanOptionalAction, default="false")
args = argparser.parse_args()

# Run the bot
if args.restore_commands == True:
    restore_commands()
else:
    # Run the bot
    logger.info('Starting TaskBot')
    bot = TaskBot()
    bot.run(config.bot['token'])
