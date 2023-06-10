from datetime import datetime, timedelta
import requests
import asyncio
from typing import Optional, Union, Tuple

import config
import utils

# ================# Functions #================ #


def compare_alarm_time(alarm_a: datetime, alarm_b: datetime) -> Tuple[bool, Optional[bool], Optional[datetime]]:
	time_a = alarm_a.time()
	time_b = alarm_b.time()

	delta_minutes: int = (time_b.minute - time_a.minute) + 60 * (time_b.hour - time_a.hour)

	return (time_a > time_b), delta_minutes

# ================# Functions #================ #


# ================# Classes #================ #


class VirtualClock:
	def __init__(self, alarms: list[datetime]) -> None:
		self.is_started: bool = False
		self.current_time: datetime = None
		self.alarms: list[datetime] = alarms

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
				
				for index, alarm in enumerate(self.alarms):
					is_past, delta_minutes = compare_alarm_time(self.current_time, alarm)
					print(index, is_past, delta_minutes)
		else:
			utils.logger.warning("Virtual clock is already running")

	def stop(self) -> None:
		utils.logging_formatter.separator("Stopping Virtual Clock")

		if self.is_started:
			utils.logger.info("Stopping virtual clock")

			self.is_started = False
		else:
			utils.logger.warning("Virtual clock is already not running")


# ================# Classes #================ #
