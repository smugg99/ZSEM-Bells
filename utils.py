import logging

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


# ================# Functions #================ #
