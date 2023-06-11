import logging
import requests
import asyncio

from datetime import datetime, time
from classes.logging_formatter import LoggingFormatter
from typing import Tuple, Optional, Union

import config

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(config.LOGS_FILE_PATH)
file_handler.setLevel(logging.INFO)

logging_formatter = LoggingFormatter()
file_handler.setFormatter(logging_formatter.raw_formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(logging_formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

# ================# Functions #================ #

logging.Logger.raw = lambda self, message, *args, **kwargs: self._log(config.LOGGER_RAW_LEVEL, message, args, **kwargs) if self.isEnabledFor(config.LOGGER_RAW_LEVEL) else None

def build_branch_url(branch_index: int) -> str:
	return config.SCHEDULE_URL + config.SCHEDULE_BRANCH_ENDPOINT.format(branch_index)

def check_website_status(url: str) -> bool:
	try:
		response: requests.Response = requests.get(url)
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
		_time : time = to_timestamp(timestamp)
		return True, _time
	except ValueError:
		return False, None

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
	def to_minutes(timestamp: time) -> int:
		return timestamp.hour * 60 + timestamp.minute + (timestamp.second / 60)
	
	minutes_a = to_minutes(timestamp_a)
	minutes_b = to_minutes(timestamp_b)

	difference = minutes_b - minutes_a

	return difference < 0, difference

# ================# Functions #================ #
