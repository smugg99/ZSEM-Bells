#!/usr/bin/env python3

import asyncio
import tracemalloc

from classes.schedule_keeper import ScheduleKeeper
from classes.virtual_clock import VirtualClock

import utils
import config

tracemalloc.start()

# ================# Functions #================ #

if __name__ == "__main__":
    print("\n# ================# Logger Test #================ #")
    utils.logger.debug("debug message test")
    utils.logger.info("info message test")
    utils.logger.warning("warning message test")
    utils.logger.error("error message test")
    utils.logger.critical("critical message test")
    print("# ================# Logger Test #================ #\n")

    virtual_clock = VirtualClock()
    schedule_keeper = ScheduleKeeper()

    try:
        schedule_keeper.sync_schedule()
    except Exception as e:
        utils.logger.error("Failed to sync the schedule keeper: " + str(e))

    try:
        asyncio.run(virtual_clock.start())
    except Exception as e:
        utils.logger.error("Failed to start the virtual clock: " + str(e))

# ================# Functions #================ #
