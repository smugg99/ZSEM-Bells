import datetime
import requests
import asyncio

import config

# ================# Classes #================ #


class VirtualClock:
    def __init__(self) -> None:
        self.is_started: bool = False
        self.current_time: datetime = None

    def sync_time(self) -> datetime:
        try:
            response = requests.get(config.TIME_API_URL, timeout=10)
            response.raise_for_status()
        except Exception as e:
            self.current_time = datetime.datetime.now()
            print(
                "Exception has been thrown while syncing time from API, using system time: " + str(self.current_time) + "\n" + str(e))
        else:
            _data = response.json()
            _current_time = datetime.datetime.strptime(
                _data["datetime"], "%Y-%m-%dT%H:%M:%S.%f%z")

            self.current_time = _current_time

            print("Time has been synced from API to: " + str(self.current_time))

        return self.current_time

    async def increment_time(self) -> None:
        while self.is_started:
            await asyncio.sleep(1)
            self.current_time += datetime.timedelta(seconds=1)

            print("Current Time:", self.current_time.strftime("%H:%M:%S"))

    async def start(self) -> None:
        if not self.is_started:
            print("Starting clock")

            self.is_started = True
            self.sync_time()

            await self.increment_time()
        else:
            print("Clock has already been started")


# ================# Classes #================ #
