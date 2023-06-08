#!/usr/bin/env python3

from classes.schedule_keeper import ScheduleKeeper
from classes.virtual_clock import VirtualClock
from classes.logging_formatter import LoggingFormatter
from tabulate import tabulate
from requests.exceptions import Timeout, ConnectionError, HTTPError
import asyncio
import tracemalloc

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
        asyncio.run(virtual_clock.start())
    except KeyboardInterrupt:
        utils.logger.warning("Program has been interrupted by the user")

# ================# Functions #================ #
