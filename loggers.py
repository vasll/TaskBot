''' Sets up the loggers for this project '''
import os
from datetime import datetime
from logger_factory import LoggerFactory


log_dir = 'logs'

discord_logger = LoggerFactory.make_logger(
    'discord', 
    f'{log_dir}/discord/{datetime.utcnow().strftime("%Y-%m-%d %H-%M-%S")}.log',
    to_stdout=False
)

logger = LoggerFactory.make_logger(
    'custom', 
    f'{log_dir}/custom/{datetime.utcnow().strftime("%Y-%m-%d %H-%M-%S")}.log'
)
