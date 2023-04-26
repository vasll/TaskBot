""" Contains some random utilities for the taskbot """
import logging
import os
import requests
from logging import Formatter
import json


# Utility variables
gmt_timezones = [
    'Etc/GMT+0', 'Etc/GMT+1', 'Etc/GMT+2', 'Etc/GMT+3', 'Etc/GMT+4', 'Etc/GMT+5', 'Etc/GMT+6', 'Etc/GMT+7',
    'Etc/GMT+8', 'Etc/GMT+9', 'Etc/GMT+10', 'Etc/GMT+11', 'Etc/GMT+12', 'Etc/GMT-1', 'Etc/GMT-2',
    'Etc/GMT-3', 'Etc/GMT-4', 'Etc/GMT-5', 'Etc/GMT-6', 'Etc/GMT-7', 'Etc/GMT-8', 'Etc/GMT-9',
    'Etc/GMT-10', 'Etc/GMT-11'
]


# Utility functions
def make_logger(
        name: str, file: str, level=logging.DEBUG, to_file=True, to_stdout=True, create_dirs=True,
        formatter=Formatter(
            f'[%(asctime)s] [%(name)s] [%(levelname)s] [%(module)s] %(message)s')
        ) -> logging.Logger:
    """ Creates and returns a new logger """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if create_dirs:
        path = os.path.dirname(os.path.abspath(file))  # Get path from file
        if not os.path.exists(path):
            os.makedirs(path)

    if to_file:
        file_handler = logging.FileHandler(file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if to_stdout:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger


def get_motivational_quote():
    """ Returns a motivational quote from api.quotable.io"""
    response = requests.get("https://api.quotable.io/quotes/random?tags=motivational")
    return json.loads(response.text)[0]
