#!/usr/bin/env python3

import asyncio

from classes.schedule_keeper import ScheduleKeeper
from classes.virtual_clock import VirtualClock

import utils
import config


# ================# Functions #================ #

async def main():
    utils.logging_formatter.startup()
    utils.logging_formatter.test()
    
    schedule_keeper = ScheduleKeeper(config.SCHEDULE_FILE_PATH)
    await schedule_keeper.sync_schedule()
    
    virtual_clock = VirtualClock(schedule_keeper.get_alarms())
    await virtual_clock.sync_time()
    
    clock_task = asyncio.create_task(virtual_clock.start_t())
    #schedule_task = asyncio.create_task(schedule_keeper.sync_schedule_t())

    # Sync everything before and after the schedule hours instead of const interval?
    while True:
        await asyncio.sleep(config.SYNC_INTERVAL)
        await schedule_keeper.sync_schedule()
        await virtual_clock.sync_time()

if __name__ == "__main__":
    asyncio.run(main())

# ================# Functions #================ #
