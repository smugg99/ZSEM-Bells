#!/usr/bin/env python3

import asyncio
import tracemalloc

from requests.exceptions import Timeout, ConnectionError, HTTPError
from tabulate import tabulate

from classes.virtual_clock import VirtualClock
from classes.schedule_keeper import ScheduleKeeper

tracemalloc.start()

# ================# Functions #================ #

if __name__ == "__main__":
    virtual_clock = VirtualClock()
    schedule_keeper = ScheduleKeeper()

    try:
        asyncio.run(virtual_clock.start())
    except KeyboardInterrupt:
        print("Program has been interrupted by the user")

# ================# Functions #================ #
