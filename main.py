#!/usr/bin/env python3

import json
import asyncio

from classes.schedule_keeper import ScheduleKeeper
from classes.virtual_clock import VirtualClock
from classes.config_manager import ConfigManager

from datetime import datetime, time
from typing import List, Optional

import utils
import config


# ================# Functions #================ #

def sync_timestamp_callback():
    print("Syncing time")

async def main():
    utils.logging_formatter.startup()
    utils.logging_formatter.test()
    
    config_manager = ConfigManager()
    config_manager.load_config(config.USER_CONFIG_FILE_PATH)
    user_config = config_manager.get_config()
    
    schedule_keeper = ScheduleKeeper(config.SCHEDULE_FILE_PATH)
    await schedule_keeper.sync_schedule()
    
    virtual_clock = VirtualClock(schedule_keeper.get_timestamps())
    await virtual_clock.sync_time()
    
    sync_timestamps: Optional[List[str]] = user_config.get("sync_timestamps", [])
    if not sync_timestamps:
        utils.logger.warn("Sync timestamps are empty")
    else:
        utils.logger.debug(sync_timestamps)
        timestamps: time = []
        for raw_timestamp in sync_timestamps:
            is_valid, timestamp = utils.is_valid_timestamp(raw_timestamp)
            print(is_valid, timestamp)
            if not is_valid:
                utils.logger.error("Invalid sync timestamp in user config file: " + str(raw_timestamp))
                continue
            
            timestamps.append(timestamp)
        
        utils.logger.debug(timestamps)
        
        virtual_clock.add_triggered_callback(timestamps, sync_timestamp_callback)
    
    clock_task = asyncio.create_task(virtual_clock.start_t())
    #schedule_task = asyncio.create_task(schedule_keeper.sync_schedule_t())

    # Sync everything before and after the schedule hours instead of const interval?
    # while True:
    #     await asyncio.sleep(config.SYNC_INTERVAL)
    #     await schedule_keeper.sync_schedule()
    #     await virtual_clock.sync_time()
        
    await clock_task

if __name__ == "__main__":
    asyncio.run(main())

# ================# Functions #================ #
