from datetime import datetime, timedelta
import requests
import asyncio

import config
import utils


# ================# Classes #================ #


class VirtualClock:
    def __init__(self) -> None:
        self.is_started: bool = False
        self.current_time: datetime = None
        self.alarms: list[datetime] = []

    def sync_time(self) -> datetime:
        try:
            response = requests.get(
                config.TIME_API_URL, timeout=config.TIME_API_REQUEST_TIMEOUT)
            response.raise_for_status()
        except Exception as e:
            self.current_time = datetime.now()
            utils.logger.error(
                "Failed to sync time from API, using system time: " + str(self.current_time) + "\n" + str(e))
        else:
            _data = response.json()
            _current_time = datetime.strptime(
                _data["datetime"], "%Y-%m-%dT%H:%M:%S.%f%z")

            self.current_time = _current_time

            utils.logger.info("Synced time from API to: " +
                              str(self.current_time))

        return self.current_time

    def increment_time(self) -> None:
        self.current_time += timedelta(seconds=1)
        utils.logger.info("Current Time: " + str(self.current_time))

    async def start(self) -> None:
        _v_c_text: str = "Starting Virtual Clock"
        utils.logging_formatter.separator(True, _v_c_text)

        if not self.is_started:
            utils.logger.info("Starting virtual clock")

            self.is_started = True
            self.sync_time()

            while self.is_started:
                self.increment_time()
                await asyncio.sleep(1)
        else:
            utils.logger.warning("Virtual clock is already running")

        utils.logging_formatter.separator(False, _v_c_text)

    async def stop(self) -> None:
        _v_c_text: str = "Stopping Virtual Clock"
        utils.logging_formatter.separator(True, _v_c_text)

        if self.is_started:
            utils.logger.info("Stopping virtual clock")

            self.is_started = False
        else:
            utils.logger.warning("Virtual clock is already not running")

        utils.logging_formatter.separator(False, _v_c_text)


# ================# Classes #================ #
