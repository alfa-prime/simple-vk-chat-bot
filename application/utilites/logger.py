import logging
import datetime

from .helpers import make_dir

def set_logger(name):
    """ задает параметры логгера"""
    make_dir('logs')

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)-23s '
                                  '%(levelname)-7s '
                                  '%(filename)-8s '
                                  '%(funcName)-14s '
                                  'line:%(lineno)-4s '
                                  '%(message)s')

    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    file = logging.FileHandler(f'logs/{now}.log', encoding='utf-8')
    file.setLevel(logging.INFO)
    file.setFormatter(formatter)
    logger.addHandler(file)

    return logger
