from datetime import datetime, timedelta, time
import requests
import asyncio
from typing import Optional, Union, Tuple, Callable, Dict, List

import config
import utils


# ================# Classes #================ #


class VirtualClock:
	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super().__new__(cls)
		return cls._instance
	
	def __init__(self) -> None:
		self.is_started: bool = False
		self.current_time: datetime = None
  
		# Internal timestamps, aquired from schedule keeper
		self._timestamps: List[time] = []
  
		# External timestamps, can be added to trigger callbacks on certain occasions
		self._callback_timestamps: List[List[List[time], Callable]] = []
  
		self.work_callback: Callable = None
		self.break_callback: Callable = None
  
	def __call__(self) -> 'VirtualClock':
		return self
	
 
	def sync_time(self) -> datetime:
		def _use_system_time(e: Exception = None) -> datetime:
			self.current_time = datetime.now()
			utils.logger.error("Failed to sync time from API, using system time: " + str(self.current_time) + ("\n" + str(e) if e else ""))
	 
		utils.logging_formatter.separator("Syncing Virtual Clock")
  
		if utils.check_website_status(config.TIME_API_URL):
			try:
				response = requests.get(
					config.TIME_API_URL, timeout=config.TIME_API_REQUEST_TIMEOUT)
				response.raise_for_status()
			except Exception as e:
				_use_system_time(e)
			else:
				_data = response.json()
				_current_time = datetime.strptime(
					_data["datetime"], "%Y-%m-%dT%H:%M:%S.%f%z")

				self.current_time = _current_time

				utils.logger.info("Synced time from API to: " +
								str(self.current_time))
		else:
			_use_system_time()

		return self.current_time

	def set_timestamps(self, timestamps: List[time]) -> None:
		self._timestamps = timestamps

	async def start_t(self) -> None:
		utils.logging_formatter.separator("Starting Virtual Clock")

		if not self.is_started:
			utils.logger.info("Starting virtual clock")

			self.is_started = True
			if not self.current_time:
				self.sync_time()

			while self.is_started:
				await asyncio.sleep(1)
	
				self.current_time += timedelta(seconds=1)
				current_timestamp: time = self.current_time.time()
				
				# Schedule timestamps, I should also add a way to distingush
				# break timestamps (every second one) and work ones (every first one)
				for index, _timestamp in enumerate(self._timestamps):
					is_past, delta_seconds = utils.compare_timestamps(current_timestamp, _timestamp)

					if is_past and delta_seconds == 0:
						if index % 2:
							self.break_callback()
						else:
							self.work_callback()
						callback()

				# Other timestamps, they may be used to synchronise things,
				# they get called on specific time objects
				for callback_timestamp in self._callback_timestamps:
					timestamps: List[time] = callback_timestamp[0]
					callback: Callable = callback_timestamp[1]

					for index, timestamp in enumerate(timestamps):
						is_past, delta_seconds = utils.compare_timestamps(current_timestamp, timestamp)

						# Note, this implementation may need to be changed in the future after tests
						# I don't know yet if the timings will be correct so it won't skip some seconds...
						if is_past and delta_seconds == 0:
							callback()

				# Print other things here, like time to sync and wb callbacks...
				# utils.logger.info("Current Time: " + str(self.current_time))
				# utils.log_table({
				# 	"Closest Timestamp": str(closest_timestamp),
				# 	"Delta Seconds": str(delta_seconds),
				# 	"Current Datetime": str(self.current_time)
				# })
    
				closest_timestamp, closest_delta_seconds = utils.get_adjacent_timestamp(self._timestamps, True)

				table_data: List[str] = [
       				"Next Timestamp",
        			"Delta Seconds",
        			"Current Datetime"
        		]
    
				headers: List[str] = [
        			utils.to_string(closest_timestamp),
           			str(closest_delta_seconds),
              		str(self.current_time.strftime("%Y-%m-%d %H:%M:%S"))
                ]

				utils.log_table((table_data, headers))
		else:
			utils.logger.warning("Virtual clock is already running")

	def stop(self) -> None:
		utils.logging_formatter.separator("Stopping Virtual Clock")

		if self.is_started:
			utils.logger.info("Stopping virtual clock")

			self.is_started = False
		else:
			utils.logger.warning("Virtual clock is already not running")

	def add_wb_callbacks(self, work_callback: Callable, break_callback: Callable) -> None:
		self.work_callback = work_callback
		self.break_callback = break_callback

	def add_timestamp_callback(self, timestamps: List[time], callback: Callable):
		self._callback_timestamps.append([timestamps, callback])


# ================# Classes #================ #
