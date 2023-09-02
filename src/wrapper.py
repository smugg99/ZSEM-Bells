import asyncio
import subprocess

from typing import Dict, Optional

import OPi.GPIO as GPIO
import utils

# Allwinner H616
#  +------+-----+----------+------+---+  Zero 2  +---+------+----------+-----+------+
#  | GPIO | wPi |   Name   | Mode | V | Physical | V | Mode | Name     | wPi | GPIO |
#  +------+-----+----------+------+---+----++----+---+------+----------+-----+------+
#  |      |     |     3.3V |      |   |  1 || 2  |   |      | 5V       |     |      |
#  |  229 |   0 |    SDA.3 |  OFF | 0 |  3 || 4  |   |      | 5V       |     |      |
#  |  228 |   1 |    SCL.3 |  OFF | 0 |  5 || 6  |   |      | GND      |     |      |
#  |   73 |   2 |      PC9 |  OFF | 0 |  7 || 8  | 0 | ALT2 | TXD.5    | 3   | 226  |
#  |      |     |      GND |      |   |  9 || 10 | 0 | ALT2 | RXD.5    | 4   | 227  |
#  |   70 |   5 |      PC6 | ALT5 | 0 | 11 || 12 | 0 | OFF  | PC11     | 6   | 75   |
#  |   69 |   7 |      PC5 | ALT5 | 0 | 13 || 14 |   |      | GND      |     |      |
#  |   72 |   8 |      PC8 |  OFF | 0 | 15 || 16 | 0 | OFF  | PC15     | 9   | 79   |
#  |      |     |     3.3V |      |   | 17 || 18 | 0 | OFF  | PC14     | 10  | 78   |
#  |  231 |  11 |   MOSI.1 | ALT4 | 0 | 19 || 20 |   |      | GND      |     |      |
#  |  232 |  12 |   MISO.1 | ALT4 | 0 | 21 || 22 | 0 | OFF  | PC7      | 13  | 71   |
#  |  230 |  14 |   SCLK.1 | ALT4 | 0 | 23 || 24 | 0 | ALT4 | CE.1     | 15  | 233  |
#  |      |     |      GND |      |   | 25 || 26 | 0 | OFF  | PC10     | 16  | 74   |
#  |   65 |  17 |      PC1 |  OFF | 0 | 27 || 28 |   |      |          |     |      |
#  |  272 |  18 |     PI16 |  OFF | 0 | 29 || 30 |   |      |          |     |      |
#  |  262 |  19 |      PI6 |  OFF | 0 | 31 || 32 |   |      |          |     |      |
#  |  234 |  20 |     PH10 | ALT3 | 0 | 33 || 34 |   |      |          |     |      |
#  +------+-----+----------+------+---+----++----+---+------+----------+-----+------+
#  | GPIO | wPi |   Name   | Mode | V | Physical | V | Mode | Name     | wPi | GPIO |
#  +------+-----+----------+------+---+  Zero 2  +---+------+----------+-----+------+


# ================# Functions #================ #

def play_wav_file(file_path):
    command = ['aplay', file_path]
    subprocess.run(command)


def setup_gpio():
    utils.logging_formatter.separator("Setting up GPIO")
    gpio_pins_enabled: Optional[bool] = utils.user_config.get(
        "gpio_pins_enabled", False)

    if gpio_pins_enabled:
        gpio_pins_config: Optional[Dict[str, int]
                                   ] = utils.user_config.get("gpio_pins", {})

        if not gpio_pins_config:
            utils.logger.warn("GPIO config is empty")
        else:
            GPIO.setboard(GPIO.H616)
            GPIO.setmode(GPIO.BOARD)

            pins_to_setup = [
                gpio_pins_config["neutral_callback"],
                gpio_pins_config["work_callback"],
                gpio_pins_config["break_callback"]
            ]

            for pin in pins_to_setup:
                try:
                    GPIO.setup(pin, GPIO.OUT, pull_up_down=GPIO.PUD_UP)
                except Exception as e:
                    utils.logger.error(
                        "GPIO pins are probably not supported on this device: " + str(e))
                else:
                    utils.logger.info("Setting pin " + str(pin) + " as output")
                    GPIO.output(pin, GPIO.HIGH)
    else:
        utils.logger.warn("GPIOs are disabled")


def cleanup_gpio():
    gpio_pins_enabled: Optional[bool] = utils.user_config.get(
        "gpio_pins_enabled", False)

    if gpio_pins_enabled:
        utils.logging_formatter.separator("Cleaning up GPIO")
        GPIO.cleanup()


async def callback_handler(is_work: bool):
    gpio_pins_enabled: Optional[bool] = utils.user_config.get(
        "gpio_pins_enabled", False)
    if not gpio_pins_enabled:
        return

    gpio_pins_config: Optional[Dict[str, int]
                               ] = utils.user_config.get("gpio_pins", {})

    if not gpio_pins_config:
        utils.logger.warn(
            "GPIO config is empty, not executing callback handler")
        return

    callback_type: str = ("work" if is_work else "break")
    gpio_pin: int = gpio_pins_config[callback_type + "_callback"]
    if not gpio_pin:
        utils.logger.warn("GPIO pins for wb callback are invalid")
        return

    GPIO.output(gpio_pin, GPIO.LOW)
    await asyncio.sleep(5)
    GPIO.output(gpio_pin, GPIO.HIGH)

    utils.logger.info("Callback of type " + callback_type + " finished")


# ================# Functions #================ #
