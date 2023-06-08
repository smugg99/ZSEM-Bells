#!/usr/bin/env python3

import datetime
import asyncio
import requests
import aiohttp
import tracemalloc

from requests.exceptions import Timeout, ConnectionError, HTTPError
from tabulate import tabulate

tracemalloc.start()

SCHEDULE_URL = "https://zsem.edu.pl/plany/"
TIME_API_URL = "http://worldtimeapi.org/api/ip"

# note for tommorow, what the fuck type is datetime.time()?? I dont want to convert it to string and later to datetime again nigga

# ================# Classes #================ #


class Clock:
    def __init__(self):
        self.is_started : bool = False
        self.current_time : datetime = None

    def sync_time(self) -> datetime:
        try:
            response = requests.get(TIME_API_URL, timeout=10)
            response.raise_for_status()
        except Exception as e:
            self.current_time = datetime.datetime.now()
            print(
                "Exception has been thrown while syncing time, using system time: " + str(e))
        else:
            _data = response.json()
            _current_time = datetime.datetime.strptime(
                _data["datetime"], "%Y-%m-%dT%H:%M:%S.%f%z")

            self.current_time = _current_time

        print("Time has been synced to: " + str(self.current_time))

        return self.current_time

    async def increment_time(self):
        while self.is_started:
            await asyncio.sleep(1)
            self.current_time += datetime.timedelta(seconds=1)
            print("Current Time:", self.current_time.strftime("%H:%M:%S"))

    async def start(self):
        if not self.is_started:
            self.is_started = True
            self.sync_time()

            await self.increment_time()
        else:
            print("Clock has already been started")


# ================# Classes #================ #

clock = Clock()
asyncio.run(clock.start())

# ================# Functions #================ #

# Get current date-time from the api, update it locally


# async def sync_time():
#     pass


# async def main():
#     pass

# ================# Functions #================ #
