""" Creates a simple-to-use logger. Made by: github.com/vasll """
import logging
import os
from logging import Formatter


def make_logger(name: str, file: str, level=logging.DEBUG, to_file=True, to_stdout=True, create_dirs=True,
                formatter=Formatter('[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s')) -> logging.Logger:
    """ Creates and returns a new logger """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if create_dirs:
        path = os.path.dirname(os.path.abspath(file))  # Get path from file
        if not os.path.exists(path):
            os.makedirs(path)

    if to_file:
        file_handler = logging.FileHandler(file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if to_stdout:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger
