import logging
import requests

from classes.logging_formatter import LoggingFormatter

import config

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(LoggingFormatter())

logger.addHandler(stream_handler)

# ================# Functions #================ #


def build_branch_url(branch_index: int) -> str:
    return config.SCHEDULE_URL + config.SCHEDULE_BRANCH_ENDPOINT.format(branch_index)


def check_website_status(url: str) -> bool:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logger.info("Website " + url + " is up and running")
            return True
        else:
            logger.error("Website " + url +
                         " is down with status code: " + str(response.status_code))
            return False
    except requests.ConnectionError:
        logger.error("Website " + url + " failed to report it\'s status")
        return False


# ================# Functions #================ #
