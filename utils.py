import logging
import requests
import asyncio

from classes.logging_formatter import LoggingFormatter

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


# ================# Functions #================ #
