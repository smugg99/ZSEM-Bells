import json
import requests
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup

import config
import utils

# note for tommorow, optimise this

# ================# Functions #================ #


def _parse_hour_range(hour_range: str):
    return hour_range.replace(" ", "").split("-")


def _extract_hour_ranges(page_content: str):
    soup = BeautifulSoup(page_content, "html.parser")
    schedule_table = soup.find(
        "table", class_=config.SCHEDULE_TABLE_CLASS_NAME)

    table_rows = schedule_table.find_all("tr")

    # Remove the first element of the table because it contains column titles
    table_rows.pop(0)

    hour_ranges: list = []
    _hour_ranges: list = []
    for table_row in table_rows:
        _hour_ranges.append(table_row.find(
            "td", class_=config.SCHEDULE_TABLE_HOUR_CLASS_NAME))

    for hour_range in _hour_ranges:
        hour_ranges.append(_parse_hour_range(hour_range.text))

    return hour_ranges


def _get_valid_branches():
    valid_branches: list = []
    branch_index: int = 1
    bad_branches_count: int = 0

    utils.logger.info(
        "Getting valid branches from base url of: " + config.SCHEDULE_URL)

    try:
        while True:
            branch_url: str = utils.build_branch_url(branch_index)

            try:
                response = requests.get(
                    branch_url, timeout=config.SCHEDULE_REQUEST_TIMEOUT)
                response.raise_for_status()
            except Exception as e:
                utils.logger.warn(
                    "Failed to get response from branch of index: " + str(branch_index) + "\n" + str(e))
                bad_branches_count += 1
            else:
                parsed_url: str = urlparse(response.request.path_url)
                query_params: dict = parse_qs(parsed_url.query)

                # "error" query parameter is specific for zsem.edu.pl
                if ("error" not in query_params) and response.status_code == 200:
                    hour_ranges = _extract_hour_ranges(response.content)

                    # Ignore the branch if it has no hour ranges
                    if len(hour_ranges) <= 0:
                        continue

                    valid_branches.append([
                        branch_index, hour_ranges
                    ])

                    utils.logger.info(
                        "Got response from a valid branch of index: " + str(branch_index) + " : " + str(response.status_code))
                else:
                    utils.logger.warn(
                        "Response returned an error query parameter: " + str(query_params))
                    bad_branches_count += 1

            branch_index += 1

            if bad_branches_count >= config.SCHEDULE_MAX_BAD_BRANCHES:
                utils.logger.warning(
                    "Max number of bad branches reached: " + str(bad_branches_count))
                break
    except Exception as e:
        utils.logger.error("Failed to get valid branches: " + str(e))

    utils.logger.info("Number of valid branches: " +
                      str(len(valid_branches)) + " : " + str(valid_branches))

    return valid_branches

# ================# Functions #================ #


# ================# Classes #================ #


class ScheduleKeeper():
    def __init__(self) -> None:
        schedule: list = []
        valid_branches: list = []

    def sync_schedule(self) -> None:
        utils.logger.info("Syncing schedule from: " + config.SCHEDULE_URL)
        if utils.check_website_status(config.MAIN_SITE):
            self.valid_branches = _get_valid_branches()

            longest_branch = None
            for branch in self.valid_branches:
                if longest_branch == None:
                    longest_branch = branch
                    continue
                elif len(longest_branch[1]) < len(branch[1]):
                    longest_branch = branch
            print(longest_branch)
        else:
            utils.logger.error("Can't sync schedule due to " +
                               config.MAIN_SITE + " being down, attempting to use the cached one...")
            # Load the json file as self.schedule


# ================# Classes #================ #
