import OPi.GPIO as GPIO
import subprocess
import asyncio

from classes.config_manager import ConfigManager
from typing import Dict, Optional

import utils

# PC6 -> Work
# PC5 -> Break
# PC8 -> Both


# ================# Functions #================ #

def play_wav_file(file_path):
	command = ['aplay', file_path]
	subprocess.run(command)

def setup_gpio():
	utils.logging_formatter.separator("Setting up GPIO")
	gpio_pins_disabled: Optional[bool] = utils.user_config.get("disable_gpio_pins", False)	

	if not gpio_pins_disabled:
		gpio_pins_config: Optional[Dict[str, int]] = utils.user_config.get("gpio_pins", {})
	
		if not gpio_pins_config:
			utils.logger.warn("GPIO config is empty")
		else:
			GPIO.setmode(GPIO.BOARD)
      
			pins_to_setup = [
				gpio_pins_config["neutral_callback"],
				gpio_pins_config["work_callback"],
				gpio_pins_config["break_callback"]
			]

			for pin in pins_to_setup:
				print(pin)
				try:
					GPIO.setup(pin, GPIO.OUT)
				except Exception as e:
					utils.logger.error("GPIO pins are probably not supported on this device: " + str(e))
					break
				else:
					utils.logger.info("Setting pin " + str(pin) + " as output")
	else:
		utils.logger.warn("GPIOs are disabled")

def cleanup_gpio():
	gpio_pins_disabled: Optional[bool] = utils.user_config.get("disable_gpio_pins", False)	

	if not gpio_pins_disabled:
		utils.logging_formatter.separator("Cleaning up GPIO")
		GPIO.cleanup()

async def callback_handler(is_work: bool):
	gpio_pins_disabled: Optional[bool] = utils.user_config.get("disable_gpio_pins", False)	
	if gpio_pins_disabled:
		return

	gpio_pins_config: Optional[Dict[str, int]] = utils.user_config.get("gpio_pins", {})
	
	if not gpio_pins_config:
		utils.logger.warn("GPIO config is empty, not executing callback handler")
		return

	gpio_pin: int = gpio_pins_config[("work" if is_work else "break") + "_callback"]
	# Check if the gpio pins are useable
	GPIO.output(gpio_pin, GPIO.HIGH)
	await asyncio.sleep(5)
	GPIO.output(gpio_pin, GPIO.LOW)



# ================# Functions #================ #