import json
import requests
from urllib.parse import urlparse, parse_qs

import config
import utils

# ================# Functions #================ #


def _get_valid_branches():
    valid_branches: list = []
    branch_index: int = 0
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
                    valid_branches.append(branch_index)
                    utils.logger.info(
                        "Got response from a valid branch of index: " + str(branch_index) + " : " + str(response.status_code))
                    utils.scrape_schedule_table(response.content)
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
        schedule: dict = None
        valid_branches: list = _get_valid_branches()
        _scraped_schedules: list = []

    def scrape_site():
        pass

    def sync_schedule() -> dict:
        pass


# ================# Classes #================ #
