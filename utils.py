import logging
from bs4 import BeautifulSoup

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


def scrape_schedule_table(page_content: str):
    soup = BeautifulSoup(page_content, "html.parser")
    schedule_tables = soup.find(
        "table", class_=config.SCHEDULE_TABLE_CLASS_NAME)
    table_rows = schedule_tables.find_all("tr")

    # Remove the first element of the table because it contains column titles
    table_rows.pop(0)

    return table_rows


# ================# Functions #================ #
