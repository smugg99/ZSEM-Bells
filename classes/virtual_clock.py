from datetime import datetime, timedelta, time
import requests
import asyncio
from typing import Optional, Union, Tuple, Callable, Dict, List

import config
import utils


# ================# Classes #================ #


class VirtualClock:
	def __init__(self, timestamps: List[str]) -> None:
		self.is_started: bool = False
		self.current_time: datetime = None
  
		# Internal timestamps, aquired from schedule keeper
		self._timestamps: List[time] = timestamps
		self._callback_timestamps: List[List[List[time], Callable]] = []

	async def sync_time(self) -> datetime:
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

	async def start_t(self) -> None:
		utils.logging_formatter.separator("Starting Virtual Clock")

		if not self.is_started:
			utils.logger.info("Starting virtual clock")

			self.is_started = True
			if not self.current_time:
				await self.sync_time()

			while self.is_started:
				await asyncio.sleep(1)
	
				self.current_time += timedelta(seconds=1)
				utils.logger.info("Current Time: " + str(self.current_time))
				
				current_timestamp : time = self.current_time.time()
    
				# Schedule timestamps, I should also add a way to distingush
				# break timestamps (every second one) and work ones (every first one)
				# for index, _timestamp in enumerate(self._timestamps):
				# 	is_past, delta_minutes = utils.compare_timestamps(current_timestamp, _timestamp)
				# 	print(index, is_past, delta_minutes)
	 
				# Other timestamps, they may be used to synchronise things,
				# they get called on specific time objects
				for callback_timestamp in self._callback_timestamps:
					timestamps : List[time] = callback_timestamp[0]
					callback : Callable = callback_timestamp[1]
					
					for timestamp in timestamps:
						is_past, delta_minutes = utils.compare_timestamps(current_timestamp, timestamp)
						print(is_past, delta_minutes)
						# if is_past:
						# 	callback()
						if delta_minutes == 0:
							callback()
		else:
			utils.logger.warning("Virtual clock is already running")

	def stop(self) -> None:
		utils.logging_formatter.separator("Stopping Virtual Clock")

		if self.is_started:
			utils.logger.info("Stopping virtual clock")

			self.is_started = False
		else:
			utils.logger.warning("Virtual clock is already not running")

	def add_triggered_callback(self, timestamps: List[time], callback: Callable):
		self._callback_timestamps.append([timestamps, callback])
		print(str(self._callback_timestamps))


# ================# Classes #================ #
