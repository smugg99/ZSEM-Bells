"""
utils.py

This Python script provides utility functions and settings related to logging,
network requests, and timestamp manipulation. It is primarily used to support
other parts of the application and enhanceits functionality.

Dependencies:
- logging: Handling logging and log formatting.
- requests: Making HTTP requests to check website status.
- datetime: Manipulating timestamps and datetime objects.
- typing: Specifying function argument and return types.
- tabulate: Formatting data into tables.

Functions and Features:
- Logging setup and custom log levels.
- Building branch URLs based on branch indices.
- Checking the status of websites and reporting their status.
- Validating and converting timestamps.
- Finding adjacent timestamps and calculating time differences.
- Logging data as formatted tables.

Note:
Customize logging levels, log file paths, and other settings in the 'config' module.

"""


import logging
import requests

from datetime import datetime, time
from typing import Dict, List, Optional, Tuple, Any
from tabulate import tabulate

import config

from classes.user_config_manager import UserConfigManager
from classes.logging_formatter import LoggingFormatter

user_config: Dict[str, Any] = UserConfigManager().get_config()

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logging_formatter = LoggingFormatter()

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(logging_formatter)

logger.addHandler(stream_handler)

if user_config["logs_enabled"]:
    file_handler = logging.FileHandler(config.LOGS_FILE_PATH)
    file_handler.setLevel(logging.INFO)

    file_handler.setFormatter(logging_formatter.log_formatter)
    logger.addHandler(file_handler)

logging.addLevelName(config.LOGGER_RAW_LEVEL, "RAW")
logging.addLevelName(config.LOGGER_LOG_LEVEL, "LOG")


# ================# Functions #================ #

logging.Logger.raw = lambda self, message, *args, **kwargs: self._log(
    config.LOGGER_RAW_LEVEL, message, args, **kwargs) if self.isEnabledFor(config.LOGGER_RAW_LEVEL) else None
logging.Logger.log = lambda self, message, *args, **kwargs: self._log(
    config.LOGGER_LOG_LEVEL, message, args, **kwargs) if self.isEnabledFor(config.LOGGER_LOG_LEVEL) else None


def build_branch_url(branch_index: int) -> str:
    return config.SCHEDULE_URL + config.SCHEDULE_BRANCH_ENDPOINT.format(branch_index)


def check_website_status(url: str) -> bool:
    try:
        response: requests.Response = requests.get(
            url, timeout=config.STATUS_REQUEST_TIMEOUT)
        if response.status_code == 200:
            logger.info("Website " + url + " is up and running")
            return True
        else:
            logger.warn("Website " + url +
                        " is down with status code: " + str(response.status_code))
            return False
    except requests.ConnectionError:
        logger.warn("Website " + url + " failed to report it\'s status")
        return False


def is_valid_timestamp(timestamp: str) -> Tuple[bool, Optional[time]]:
    try:
        _time: time = to_timestamp(timestamp)
        return True, _time
    except ValueError:
        return False, None


def get_adjacent_timestamp(timestamps: List[time], current_timestamp: time, be_next: bool = False) -> Optional[Tuple[time, int, int]]:
    closest_timestamp: time = None
    lowest_delta_seconds: int = None
    its_index: int = None

    for index, timestamp in enumerate(timestamps):
        is_past, delta_seconds = compare_timestamps(
            current_timestamp, timestamp)

        if (be_next and is_past) or (not be_next and not is_past):
            continue

        if closest_timestamp is not None:
            if (be_next and delta_seconds > lowest_delta_seconds) or (not be_next and delta_seconds <= lowest_delta_seconds):
                continue

        lowest_delta_seconds = delta_seconds
        closest_timestamp = timestamp
        its_index = index

    if closest_timestamp is None:
        its_index = 0 if be_next else len(timestamps) - 1
        closest_timestamp = timestamps[its_index]
        _, delta_seconds = compare_timestamps(
            current_timestamp, closest_timestamp)
        lowest_delta_seconds = delta_seconds

    return closest_timestamp, lowest_delta_seconds, its_index


def to_string(timestamp: time) -> Optional[str]:
    date_obj = datetime.now().date()
    datetime_obj = datetime.combine(date_obj, timestamp)

    # Can't decide what to do here yet...
    try:
        # Try parsing timestamp without seconds
        return datetime.strftime(datetime_obj, "%H:%M:%S")
    except ValueError:
        try:
            # Try parsing timestamp with seconds
            return datetime.strftime(datetime_obj, "%H:%M")
        except ValueError:
            return None


def to_timestamp(timestamp: str) -> Optional[time]:
    try:
        # Try parsing timestamp with seconds
        return datetime.strptime(timestamp, "%H:%M:%S").time()
    except ValueError:
        try:
            # Try parsing timestamp without seconds
            return datetime.strptime(timestamp, "%H:%M").time()
        except ValueError:
            return None


def compare_timestamps(timestamp_a: time, timestamp_b: time) -> Tuple[bool, float]:
    def to_seconds(timestamp: time) -> int:
        return (timestamp.hour * 3600) + (timestamp.minute * 60) + timestamp.second

    seconds_a = to_seconds(timestamp_a)
    seconds_b = to_seconds(timestamp_b)

    delta_seconds = seconds_b - seconds_a

    return delta_seconds <= 0, delta_seconds


def log_table(data: List, headers: List[str] = "firstrow"):
    logger.raw(tabulate(data, headers=headers,
               tablefmt="fancy_grid", stralign="center"))

# ================# Functions #================ #
