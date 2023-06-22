#!/usr/bin/env python3

import asyncio
from datetime import datetime, time
from typing import List, Optional

from tabulate import tabulate

import config
import utils
import wrapper
from classes.config_manager import ConfigManager
from classes.schedule_keeper import ScheduleKeeper
from classes.virtual_clock import VirtualClock

# ================# Functions #================ #

async def main():
	utils.logging_formatter.startup()
	utils.logging_formatter.test()

	schedule_keeper = ScheduleKeeper()
	virtual_clock = VirtualClock()

	# ================# Local Functions #================ #

	def break_callback():
		utils.logger.info("Break callback triggered")
		asyncio.create_task(wrapper.callback_handler(False))

	def work_callback():
		utils.logger.info("Work callback triggered")
		asyncio.create_task(wrapper.callback_handler(True))

	def update():
		schedule_keeper.sync_schedule()
		
		virtual_clock.sync_time()
		virtual_clock.set_timestamps(schedule_keeper.get_timestamps())

 	# ================# Local Functions #================ #
  
	wrapper.setup_gpio()
	update()
 
	# Remove after tests...
	virtual_clock.current_time = datetime(2023, 5, 15, 7, 44, 50)
	virtual_clock.add_wb_callbacks(work_callback, break_callback)	

	clock_task = asyncio.create_task(virtual_clock.start_t())
	sync_timestamps: Optional[List[str]] = utils.user_config.get("sync_timestamps", [])
 
	if not sync_timestamps:
		utils.logger.warn("Sync timestamps are empty")
	else:
		timestamps: time = []
		for raw_timestamp in sync_timestamps:
			is_valid, timestamp = utils.is_valid_timestamp(raw_timestamp)
   
			if not is_valid:
				utils.logger.error("Invalid sync timestamp in user config file: " + str(raw_timestamp))
				continue
			
			timestamps.append(timestamp)
		
		parsed_timestamps: List[str] = []
		for timestamp in timestamps:
			parsed_timestamps.append(utils.to_string(timestamp))

		# Note: make the sync tables vertical instead of retarded horizontal
		table_data: List[str] = ["Sync Timestamps"]
		headers: List[str] = parsed_timestamps

		utils.log_table((table_data, headers))
  
		virtual_clock.add_timestamp_callback(timestamps, update)
		
	await clock_task

if __name__ == "__main__":
	asyncio.run(main())
	wrapper.cleanup_gpio()

# ================# Functions #================ #
