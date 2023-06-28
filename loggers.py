""" Sets up the loggers for the TaskBot project """
from datetime import datetime
import logging
import os


def make_logger(
    name: str, file: str, level=logging.DEBUG, to_file=True, to_stdout=True, create_dirs=True,
    formatter=logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] [%(module)s] %(message)s')
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


# Loggers configurations
LOGS_DIR = 'logs'
discord_logger = make_logger(
    name='discord',
    file=f'{LOGS_DIR}/discord/{datetime.utcnow().strftime("%Y-%m-%d %H-%M-%S")}.log',
    to_stdout=False
)

sqlalchemy_logger = make_logger(
    name='sqlalchemy.engine.Engine',
    file=f'{LOGS_DIR}/sqlalchemy/{datetime.utcnow().strftime("%Y-%m-%d %H-%M-%S")}.log'
)

logger = make_logger(
    name='custom',
    file=f'{LOGS_DIR}/custom/{datetime.utcnow().strftime("%Y-%m-%d %H-%M-%S")}.log'
)
