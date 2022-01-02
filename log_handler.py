import logging
from merry import Merry
import os

logs_dir = "./logs"


def create_logger(name, filename="info.log"):
    """
    Utility function to handle logging info
    :param name: The name of the logger
    :param filename: The filename to which logs are saved
    :return: Logger object
    """
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    logger = logging.getLogger(name=name)
    logger.setLevel(logging.INFO)
    log_handler = logging.FileHandler(filename=f"{logs_dir}/{filename}", mode='a+')
    formatter = logging.Formatter('[%(asctime)s] %(levelname)-8s %(filename)s %(funcName)s %(message)s')
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)

    return logger


def create_merry_object(name, filename="errors.log"):
    """
    Create merry object and log handler to inspect errors and log them
    :return: Merry object
    """
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    logger = logging.getLogger(name)
    logger.setLevel(logging.ERROR)
    merry = Merry(name)
    log_handler = logging.FileHandler(filename=f"{logs_dir}/{filename}", mode='a+')
    formatter = logging.Formatter('[%(asctime)s] %(levelname)-8s %(filename)s %(funcName)s %(message)s')
    log_handler.setFormatter(formatter)
    merry.logger.addHandler(log_handler)
    return merry


merry = create_merry_object(__name__)

@merry._except(Exception)
def handle_type_error():
    pass
