import asyncio
import requests

from datetime import datetime, time, timedelta
from typing import Callable, Dict, List, Optional, Tuple, Union

import config
import utils
import wrapper


# ================# Classes #================ #


class VirtualClock:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.is_started: bool = False
        self.current_time: datetime = None
        self.is_weekend: bool = False

        # Internal timestamps, aquired from schedule keeper
        self._timestamps: List[time] = []

        # External timestamps, can be added to trigger callbacks on certain occasions
        self._callback_timestamps: List[List[List[time], Callable]] = []

        self.work_callback: Callable = None
        self.break_callback: Callable = None
        self.neutral_callback: Callable = None

    def __call__(self) -> 'VirtualClock':
        return self

    def set_timestamps(self, timestamps: List[time]):
        self._timestamps = timestamps

    async def sync_time(self) -> datetime:
        utils.logging_formatter.separator("Syncing Virtual Clock")
        clock_sync_enabled: Optional[bool] = utils.user_config.get(
            "clock_sync_enabled", False)

        # ================# Local Functions #================ #

        def _use_system_time(e: Exception = None) -> datetime:
            self.current_time = datetime.now()
            if not clock_sync_enabled:
                utils.logger.warn("Syncing clock is disabled")
            else:
                utils.logger.error("Failed to sync time from API, using system time: " +
                                   str(self.current_time) + ("\n" + str(e) if e else ""))
                wrapper.toggle_status_led(wrapper.StatusLed.INTERNET_ACCESS, False)

        # def _use_rtc_time():
        #     pass

        # ================# Local Functions #================ #

        if clock_sync_enabled and utils.check_website_status(config.TIME_API_URL):
            try:
                response = requests.get(
                    config.TIME_API_URL, timeout=config.TIME_API_REQUEST_TIMEOUT)
                response.raise_for_status()
            except Exception as e:
                _use_system_time(e)
            else:
                _data = response.json()
                _current_time = datetime.strptime(
                    _data["datetime"], "%Y-%m-%dT%H:%M:%S.%f%z")
                _unix_timestamp = _data["unixtime"]

                self.is_weekend = utils.is_weekend(_unix_timestamp)
                self.current_time = _current_time

                utils.logger.info("Synced time from API to: " + str(self.current_time) + " Weekend: " + str(self.is_weekend))
                
                wrapper.toggle_status_led(wrapper.StatusLed.INTERNET_ACCESS)
        else:
            _use_system_time()

        return self.current_time

    async def start_t(self):
        utils.logging_formatter.separator("Starting Virtual Clock")

        if not self.is_started:
            utils.logger.info("Starting virtual clock")

            self.is_started = True
            if not self.current_time:
                await self.sync_time()

            self.log_status_table()

            _repetition: int = 0
            _loop = asyncio.get_event_loop()

            while self.is_started:
                before_sleep_time: float = _loop.time()
                current_timestamp: time = self.current_time.time()

                # Schedule timestamps
                for index, _timestamp in enumerate(self._timestamps):
                    is_past, delta_seconds = utils.compare_timestamps(
                        current_timestamp, _timestamp)

                    if is_past and delta_seconds == 0:
                        if callable(self.neutral_callback):
                            self.neutral_callback()

                        if index % 2 == 0:
                            asyncio.create_task(self.break_callback())
                        else:
                            asyncio.create_task(self.work_callback())

                # Other timestamps, they may be used to synchronise things,
                # they get called on specific timestamps
                for callback_timestamp in self._callback_timestamps:
                    timestamps: List[time] = callback_timestamp[0]
                    callback: Callable = callback_timestamp[1]

                    for index, timestamp in enumerate(timestamps):
                        is_past, delta_seconds = utils.compare_timestamps(
                            current_timestamp, timestamp)

                        # Note, this implementation may need to be changed in the future after tests
                        # I don't know yet if the timings will be correct so it won't skip some seconds...
                        if is_past and delta_seconds == 0:
                            asyncio.create_task(callback())

                if utils.user_config.get("wasteful_debug_enabled"):
                    self.log_status_table()
                else:
                    if _repetition >= config.CLOCK_RUNNING_ANNOUNCE_INTERVAL:
                        self.log_status_table()
                        _repetition = 0

                    _repetition += 1

                await asyncio.sleep(1)

                after_sleep_time: float = _loop.time()

                # Actual time slept is used here to compensate for the time drift
                # caused by the lack of the external RTC module, it doesn't interfere
                # with functions that compare timestamps and calculate their delta
                # because they operate only on hours, minutes and seconds
                actual_time_slept: float = after_sleep_time - before_sleep_time

                self.current_time += timedelta(seconds=actual_time_slept)
        else:
            utils.logger.warning("Virtual clock is already running")

    def stop(self):
        utils.logging_formatter.separator("Stopping Virtual Clock")

        if self.is_started:
            utils.logger.info("Stopping virtual clock")

            self.is_started = False
        else:
            utils.logger.warning("Virtual clock is already not running")

    # This needs testing when ill sober up
    def log_status_table(self):
        current_time = self.current_time.time()
        next_timestamp, next_delta_seconds, its_index = utils.get_adjacent_timestamp(
            self._timestamps, current_time, True)
        previous_timestamp, previous_delta_seconds, _its_index = utils.get_adjacent_timestamp(
            self._timestamps, current_time, False)

        next_timestamp_string = utils.to_string(
            next_timestamp) if next_timestamp else "None"
        next_delta_seconds_string = str(
            next_delta_seconds) if next_delta_seconds else "None"
        next_type_string = "Break" if its_index and its_index % 2 else "Work"

        previous_timestamp_string = utils.to_string(
            previous_timestamp) if previous_timestamp else "None"
        previous_delta_seconds_string = str(
            previous_delta_seconds) if previous_delta_seconds else "None"
        previous_type_string = "Break" if _its_index and _its_index % 2 else "Work"

        table_data = [
            ["Timestamp", "Delta Seconds", "Action", "Current Datetime"],
            [next_timestamp_string, next_delta_seconds_string, next_type_string,
             self.current_time.strftime("%Y-%m-%d %H:%M:%S")],
            [previous_timestamp_string,
             previous_delta_seconds_string, previous_type_string, "Is weekend: " + str(self.is_weekend)]
        ]

        utils.log_table(table_data)

    def add_wb_callbacks(self, work_callback: Callable, break_callback: Callable, neutral_callback: Callable = None):
        self.work_callback = work_callback
        self.break_callback = break_callback

        self.neutral_callback = neutral_callback

    def add_timestamp_callback(self, timestamps: List[time], callback: Callable):
        self._callback_timestamps.append([timestamps, callback])


# ================# Classes #================ #
