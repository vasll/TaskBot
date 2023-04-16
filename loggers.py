""" Sets up the loggers for this project """
from datetime import datetime
from utils.logger_factory import make_logger


log_dir = 'logs'

discord_logger = make_logger(
    name='discord',
    file=f'{log_dir}/discord/{datetime.utcnow().strftime("%Y-%m-%d %H-%M-%S")}.log',
    to_stdout=False
)

sqlalchemy_logger = make_logger(
    name='sqlalchemy.engine.Engine',
    file=f'{log_dir}/sqlalchemy/{datetime.utcnow().strftime("%Y-%m-%d %H-%M-%S")}.log'
)

logger = make_logger(
    name='custom',
    file=f'{log_dir}/custom/{datetime.utcnow().strftime("%Y-%m-%d %H-%M-%S")}.log'
)
