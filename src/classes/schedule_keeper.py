import asyncio
import json
import requests

from datetime import datetime, time
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from urllib.parse import parse_qs, urlparse
from bs4 import BeautifulSoup
from tabulate import tabulate

import config
import utils


# ================# Functions #================ #


def _parse_hour_range(hour_range: str) -> List[str]:
    return hour_range.replace(" ", "").split("-")


def _extract_hour_ranges(page_content: str, branch_index: int) -> Optional[List[str]]:
    soup = BeautifulSoup(page_content, "html.parser")
    schedule_table = soup.find(
        "table", class_=config.SCHEDULE_TABLE_CLASS_NAME)

    if schedule_table is None:
        utils.logger.warning(
            "Schedule table not found in branch of index: " + str(branch_index))
        return

    table_rows = schedule_table.find_all("tr")

    if len(table_rows) <= config.SCHEDULE_TABLE_MIN_ROWS:
        utils.logger.warning(
            "Schedule table of index {} has not enough table rows to be considered valid".format(branch_index))
        pass

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


def _get_valid_branches() -> Tuple[List[int], List[str], int]:
    valid_branches: List[int] = []
    longest_hour_ranges: List[str] = []

    _branch_index: int = 0
    _schedule_branch: int = None
    _bad_branches_count: int = 0

    utils.logger.info(
        "Getting valid branches from base url of: " + config.SCHEDULE_URL)

    try:
        while True:
            branch_url: str = utils.build_branch_url(_branch_index)

            try:
                response = requests.get(
                    branch_url, timeout=config.SCHEDULE_REQUEST_TIMEOUT)
                response.raise_for_status()
            except Exception as e:
                utils.logger.warn(
                    "Failed to get response from branch of index: " + str(_branch_index) + "\n" + str(e))
                _bad_branches_count += 1
            else:
                parsed_url: str = urlparse(response.request.path_url)
                query_params: dict = parse_qs(parsed_url.query)

                # "error" query parameter is specific for zsem.edu.pl
                if ("error" not in query_params) and response.status_code == 200:
                    hour_ranges = _extract_hour_ranges(
                        response.content, _branch_index)

                    if hour_ranges is None:
                        continue

                    valid_branches.append(_branch_index)

                    if not longest_hour_ranges or len(longest_hour_ranges) <= len(hour_ranges):
                        longest_hour_ranges = hour_ranges
                        _schedule_branch = _branch_index

                    utils.logger.info(
                        "Got response from a valid branch of index: " + str(_branch_index) + " : " + str(response.status_code))
                else:
                    utils.logger.warn(
                        "Response returned an error query parameter: " + str(query_params))
                    _bad_branches_count += 1

            _branch_index += 1

            if _bad_branches_count >= config.SCHEDULE_MAX_BAD_BRANCHES:
                utils.logger.warning(
                    "Max number of bad branches reached: " + str(_bad_branches_count))
                break
    except Exception as e:
        utils.logger.error("Failed to get valid branches: " + str(e))

    return valid_branches, longest_hour_ranges, _schedule_branch


# ================# Functions #================ #


# ================# Classes #================ #


class ScheduleKeeper():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.file_path: str = config.SCHEDULE_FILE_PATH

        self.schedule: List[str] = []
        self.schedule_branch: int = []
        self.valid_branches: List[int] = []

    def __call__(self) -> 'ScheduleKeeper':
        return self

    def read_schedule_file(self) -> Optional[Dict[str, Any]]:
        with open(self.file_path, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                utils.logger.critical("Failed to decode schedule file")
                raise
            else:
                if len(data) <= 0:
                    utils.logger.critical("Schedule file is empty")
                    raise

                # Reconsider this?
                if isinstance(data, dict):
                    return data
                else:
                    utils.logger.critical("Invalid data in the schedule file")
                    raise TypeError()

    def write_schedule_file(self, data: Dict[str, Any]):
        with open(self.file_path, "w") as file:
            json.dump(data, file)

    def sync_schedule(self) -> List[str]:
        utils.logging_formatter.separator("Syncing Schedule")

        schedule_sync_enabled: Optional[bool] = utils.user_config.get(
            "schedule_sync_enabled", False)

        if schedule_sync_enabled and utils.check_website_status(config.MAIN_SITE):
            utils.logger.info(
                "Trying to sync schedule from: " + config.SCHEDULE_URL)

            self.valid_branches, self.schedule, self.schedule_branch = _get_valid_branches()

            self.write_schedule_file({
                "valid_branches": self.valid_branches,
                "schedule_branch": self.schedule_branch,
                "schedule": self.schedule
            })

            # Compare fetched data to the cached one?
        else:
            if not schedule_sync_enabled:
                utils.logger.warn("Syncing schedule is disabled")
            else:
                utils.logger.error("Can't sync schedule due to " + config.MAIN_SITE +
                                   " being down, attempting to use the saved one...")

            data: List[str] = self.read_schedule_file()

            self.schedule_branch = data["schedule_branch"]
            self.schedule = data["schedule"]
            self.valid_branches = data["valid_branches"]

        return self.schedule

    def get_schedule(self) -> List[str]:
        return self.schedule

    def get_timestamps(self) -> List[time]:
        timestamps: List[time] = []

        for schedule_hours in self.schedule:
            for schedule_hour in schedule_hours:
                timestamps.append(utils.to_timestamp(schedule_hour))

        return sorted(timestamps)


# ================# Classes #================ #
