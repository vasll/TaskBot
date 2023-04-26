""" Sets up the loggers for the TaskBot project """
from datetime import datetime
from taskbot_utils import make_logger


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
