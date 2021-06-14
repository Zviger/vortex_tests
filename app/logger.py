"""
This module provides functions to work with logging.
"""
import logging
import sys
from logging import Logger

logger = None


def init_logger(name: str) -> Logger:
    """
    Initialize and return logger object.
    :param name: Name of the logger object.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    # create the logging file handler
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    # add handler to logger object
    logger.addHandler(stream_handler)
    return logger


def get_logger() -> Logger:
    """
    Return logger object.
    :param name: Name of the logger object.
    """
    global logger
    if not logger:
        logger = init_logger("Vortex test system")
    return logger
