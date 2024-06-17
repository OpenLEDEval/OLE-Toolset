"""
OpenLEDEval (ole) utilities
"""

import logging
import sys
from datetime import datetime

BASE_LOGGER_NAME = "ole"

__all__ = ["get_logger", "get_valid_filename"]


def get_logger(name: str = "") -> logging.Logger:
    """Create a logger for the ole module

    Parameters
    ----------
    name : str, default ""
        Names a sub-logger for level management. Default "" returns base logger
        for ole

    Returns
    -------
    logging.Logger
    """
    if name == "":
        return logging.getLogger(f"{BASE_LOGGER_NAME}")
    return logging.getLogger(f"{BASE_LOGGER_NAME}.{name}")


SYSTEM_TIME_ZONE = tz = datetime.now().astimezone().tzinfo


def datetime_now() -> datetime:
    """Return time zone aware datetime object

    Returns
    -------
    datetime
    """

    return datetime.now(tz=SYSTEM_TIME_ZONE)


BASE_LOGGER = get_logger()
BASE_LOGGER.setLevel("INFO")
BASE_LOGGER.addHandler(logging.StreamHandler(sys.stdout))
