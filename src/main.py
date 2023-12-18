#!/usr/bin/env python3

import asyncio

from datetime import datetime, time
from typing import List, Optional
from tabulate import tabulate

import config
import utils
import wrapper

from classes.schedule_keeper import ScheduleKeeper
from classes.virtual_clock import VirtualClock


# ================# Functions #================ #

async def main(gpio_setup_good: bool):
    utils.logging_formatter.startup()
    utils.logging_formatter.test()

    schedule_keeper = ScheduleKeeper()
    virtual_clock = VirtualClock()

    clock_sync_after_callbacks_enabled: Optional[bool] = utils.user_config.get(
        "clock_sync_after_callbacks_enabled", False)
    
    wrapper.toggle_status_led(wrapper.StatusLed.SUCCESS)
    
    
    # ================# Local Functions #================ #

    # Note: Add lambdas here

    async def break_callback():
        try:
            utils.logger.info("Break callback triggered")
            await wrapper.callback_handler(False, gpio_setup_good)

            if clock_sync_after_callbacks_enabled:
                asyncio.create_task(virtual_clock.sync_time())
        except Exception as e:
            wrapper.handle_error(e)

    async def work_callback():
        try:
            utils.logger.info("Work callback triggered")
            await wrapper.callback_handler(True, gpio_setup_good)

            if clock_sync_after_callbacks_enabled:
                asyncio.create_task(virtual_clock.sync_time())
        except Exception as e:
            wrapper.handle_error(e)

    async def update():
        try:
            _schedule: List[str] = schedule_keeper.sync_schedule()
            utils.log_table(_schedule)

            await virtual_clock.sync_time()
            virtual_clock.set_timestamps(schedule_keeper.get_timestamps())
        except Exception as e:
            wrapper.handle_error(e)

    # ================# Local Functions #================ #

    await update()

    # Note: remove after testing!
    virtual_clock.current_time = datetime(2023, 9, 29, 6, 59, 55)
    virtual_clock.add_wb_callbacks(work_callback, break_callback)

    clock_task = asyncio.create_task(virtual_clock.start_t())
    sync_timestamps: Optional[List[str]] = utils.user_config.get(
        "sync_timestamps", [])

    if not sync_timestamps:
        utils.logger.warn("Sync timestamps are empty")
        wrapper.toggle_status_led(wrapper.StatusLed.WARNING)
    else:
        timestamps: List[time] = []

        # Validate all sync timestamps
        for raw_timestamp in sync_timestamps:
            is_valid, timestamp = utils.is_valid_timestamp(raw_timestamp)

            if not is_valid:
                utils.logger.error(
                    "Invalid timestamp in user config: " + str(raw_timestamp))
                wrapper.toggle_status_led(wrapper.StatusLed.WARNING)
                continue

            timestamps.append(timestamp)

        utils.log_table([[utils.to_string(timestamp)
                        for timestamp in timestamps]], [])

        virtual_clock.add_timestamp_callback(timestamps, update)

    await clock_task

if __name__ == "__main__":
    try:
        gpio_setup_good: bool = wrapper.setup_gpio_pins()
        
        for status_led in wrapper.StatusLed:
            wrapper.toggle_status_led(status_led, False)

        asyncio.run(main(gpio_setup_good))
    except Exception as e:
        wrapper.handle_error(e)

# ================# Functions #================ #
