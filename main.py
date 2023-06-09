#!/usr/bin/env python3

import time
import asyncio
import tracemalloc

from classes.schedule_keeper import ScheduleKeeper
from classes.virtual_clock import VirtualClock

import utils
import config

tracemalloc.start()

# ================# Functions #================ #


async def main():
    utils.logging_formatter.test()

    virtual_clock = VirtualClock()
    schedule_keeper = ScheduleKeeper()

    try:
        schedule_keeper.sync_schedule()
    except Exception as e:
        utils.logger.error("Failed to sync the schedule keeper: " + str(e))

    try:
        asyncio.create_task(virtual_clock.start())
    except Exception as e:
        utils.logger.error("Failed to start the virtual clock: " + str(e))

# note for tommorow, learn how to handle coroutines and async shit
    await asyncio.sleep(5)
    await virtual_clock.stop()

    await asyncio.sleep(5)
    await virtual_clock.start()

    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())

# ================# Functions #================ #
