"""
wrapper.py

This script is a Python program designed to facilitate various tasks related to audio playback and GPIO
control on devices with an Allwinner H616 processor, such as the "Orange Pi Zero 2." It offers functions
for playing WAV audio files, setting up and cleaning up GPIO pins, and handling callbacks for "work" and "break" events.

Dependencies:
- os: Interaction with the operating system for file manipulation and system commands.
- subprocess: Running external processes, particularly for playing audio files.
- threading: Creating separate threads for audio playback.
- time.sleep: Introducing delays, especially during audio playback and GPIO control.
- typing.Dict and typing.Optional: Specifying function argument and return types.
- OPi.GPIO: Interacting with GPIO pins on the Orange Pi platform.

Usage:
- Import and use this script as part of a larger application or automation system.
- Customize GPIO pin configurations and other settings in the utils.user_config
dictionary for your specific hardware and use case.

Functions:
- play_wav_async(wav_filename: str): Play a WAV audio file in a asynchronous manner.
- setup_gpio_pins() -> bool: Set up GPIO pins for callbacks and check if GPIO pins are enabled.
- cleanup_gpio(): Clean up GPIO pins, releasing associated resources.
- callback_handler(is_work: bool, gpio_setup_good: bool): Handle "work" or "break" callbacks,
playing audio and controlling GPIO pins based on user configuration.

Allwinner H616
 +------+-----+----------+------+---+  Zero 2  +---+------+----------+-----+------+
 | GPIO | wPi |   Name   | Mode | V | Physical | V | Mode | Name     | wPi | GPIO |
 +------+-----+----------+------+---+----++----+---+------+----------+-----+------+
 |      |     |     3.3V |      |   |  1 || 2  |   |      | 5V       |     |      |
 |  229 |   0 |    SDA.3 |  OFF | 0 |  3 || 4  |   |      | 5V       |     |      |
 |  228 |   1 |    SCL.3 |  OFF | 0 |  5 || 6  |   |      | GND      |     |      |
 |   73 |   2 |      PC9 |  OFF | 0 |  7 || 8  | 0 | ALT2 | TXD.5    | 3   | 226  |
 |      |     |      GND |      |   |  9 || 10 | 0 | ALT2 | RXD.5    | 4   | 227  |
 |   70 |   5 |      PC6 | ALT5 | 0 | 11 || 12 | 0 | OFF  | PC11     | 6   | 75   |
 |   69 |   7 |      PC5 | ALT5 | 0 | 13 || 14 |   |      | GND      |     |      |
 |   72 |   8 |      PC8 |  OFF | 0 | 15 || 16 | 0 | OFF  | PC15     | 9   | 79   |
 |      |     |     3.3V |      |   | 17 || 18 | 0 | OFF  | PC14     | 10  | 78   |
 |  231 |  11 |   MOSI.1 | ALT4 | 0 | 19 || 20 |   |      | GND      |     |      |
 |  232 |  12 |   MISO.1 | ALT4 | 0 | 21 || 22 | 0 | OFF  | PC7      | 13  | 71   |
 |  230 |  14 |   SCLK.1 | ALT4 | 0 | 23 || 24 | 0 | ALT4 | CE.1     | 15  | 233  |
 |      |     |      GND |      |   | 25 || 26 | 0 | OFF  | PC10     | 16  | 74   |
 |   65 |  17 |      PC1 |  OFF | 0 | 27 || 28 |   |      |          |     |      |
 |  272 |  18 |     PI16 |  OFF | 0 | 29 || 30 |   |      |          |     |      |
 |  262 |  19 |      PI6 |  OFF | 0 | 31 || 32 |   |      |          |     |      |
 |  234 |  20 |     PH10 | ALT3 | 0 | 33 || 34 |   |      |          |     |      |
 +------+-----+----------+------+---+----++----+---+------+----------+-----+------+
 | GPIO | wPi |   Name   | Mode | V | Physical | V | Mode | Name     | wPi | GPIO |
 +------+-----+----------+------+---+  Zero 2  +---+------+----------+-----+------+
"""

import asyncio
import os
import pygame

from typing import Dict, Optional, List
from asyncio.subprocess import Process

import OPi.GPIO as GPIO
import utils
import config


# ================# Functions #================ #

async def play_wav_async(wav_filename: str):
    project_root = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ".."))

    wav_file_path = os.path.join(
        project_root, config.SOUNDS_FOLDER_PATH, wav_filename)

    aplay_command = ["aplay", "-D", config.DEFAULT_AUDIO_DEVICE, wav_file_path]

    try:
        process: Process = await asyncio.create_subprocess_exec(*aplay_command)

        # Wait for the process to complete with a timeout
        await asyncio.wait_for(process.wait(), timeout=config.MAX_SOUND_DURATION)

    except asyncio.TimeoutError:
        # Handle TimeoutError separately
        print(f"Timeout while playing {wav_filename}")

        # Terminate the process if it's still running
        process.terminate()
        await process.wait()  # Wait for the process to terminate

    except Exception as e:
        # Handle other exceptions
        print(f"Error playing {wav_filename}: {e}")
        raise e

async def _play_wav_async(wav_filename: str):
    try:
        # Get the project root directory
        project_root: str = os.path.abspath(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), ".."))

        # Construct the path to the WAV file based on the config_dir and sound_filename
        wav_file_path: str = os.path.join(
            project_root, config.SOUNDS_FOLDER_PATH, wav_filename)
        
        pygame.mixer.init()
        print(wav_file_path)
        pygame.mixer.music.load(wav_file_path)
        pygame.mixer.music.play()
        
        await asyncio.sleep(config.MAX_SOUND_DURATION)
        
        pygame.mixer.quit()
    except Exception as e:
        print(e)
        raise(e)


# Note: This should actually be called setup callback pins or something
def setup_gpio_pins() -> bool:
    utils.logging_formatter.separator("Setting up GPIO")
    gpio_pins_enabled: Optional[bool] = utils.user_config.get(
        "gpio_pins_enabled", False)

    if gpio_pins_enabled:
        gpio_pins_config: Optional[Dict[str, int]
                                   ] = utils.user_config.get("gpio_pins", {})

        _outputs_config: Optional[Dict[str, int]
                                  ] = gpio_pins_config.get("outputs", {})

        # _outputs_config: Optional[Dict[str, int]
        #                           ] = gpio_pins_config.get("outputs", {})
        # _inputs_config: Optional[Dict[str, int]
        #                          ] = gpio_pins_config.get("inputs", {})

        if not gpio_pins_config or not _outputs_config:
            utils.logger.warn("GPIO config is empty")
            return False
        else:
            GPIO.setboard(GPIO.H616)
            GPIO.setmode(GPIO.BOARD)

            pins_to_setup = [
                _outputs_config["neutral_callback"],
                _outputs_config["work_callback"],
                _outputs_config["break_callback"]
            ]

            for pin in pins_to_setup:
                try:
                    GPIO.setup(pin, GPIO.OUT)
                except Exception as e:
                    print(e)
                    return False
                else:
                    utils.logger.log("Setting gpio " + str(pin) + " as OUTPUT")
                    GPIO.output(pin, GPIO.LOW)

        return True
    else:
        utils.logger.warn("GPIOs are disabled")
        return False


def cleanup_gpio():
    gpio_pins_enabled: Optional[bool] = utils.user_config.get(
        "gpio_pins_enabled", False)

    if gpio_pins_enabled:
        utils.logging_formatter.separator("Cleaning up GPIO")
        GPIO.cleanup()


async def callback_handler(is_work: bool, gpio_setup_good: bool):
    gpio_pins_enabled: Optional[bool] = utils.user_config.get(
        "gpio_pins_enabled", False)

    gpio_pins_config: Optional[Dict[str, int]
                               ] = utils.user_config.get("gpio_pins", {})

    outputs: Optional[Dict[str, int]] = gpio_pins_config.get("outputs", {})

    _callback_type: str = ("work" if is_work else "break")
    _gpio_good: bool = False

    if gpio_pins_enabled and gpio_setup_good:
        if not gpio_pins_config or not outputs:
            utils.logger.warn(
                "GPIO config is empty, not changing any states")
        else:
            gpio_pin: int = outputs[_callback_type + "_callback"]
            neutral_gpio_pin: int = outputs["neutral_callback"]

            if not gpio_pin or not neutral_gpio_pin:
                utils.logger.warn("GPIO pins for wb callback are invalid")
            else:
                _gpio_good = True
                _gpio_value: bool = GPIO.HIGH

                utils.logger.log("GPIO " + str(gpio_pin) + " is ON!")
                GPIO.output(gpio_pin, _gpio_value)
                GPIO.output(neutral_gpio_pin, _gpio_value)

    if utils.user_config["sounds_enabled"]:
        _bell_sound_filename: str = utils.user_config["bell_sounds"][_callback_type]
        utils.logger.info("Sound should be playing right now!")
        await play_wav_async(_bell_sound_filename)
    else:
        utils.logger.info("Delay should be performed right now!")
        await asyncio.sleep(config.MAX_BELL_DURATION)

    if _gpio_good and gpio_setup_good:
        _gpio_value: bool = GPIO.LOW

        utils.logger.log("GPIO " + str(gpio_pin) + " is OFF!")
        GPIO.output(gpio_pin, _gpio_value)
        GPIO.output(neutral_gpio_pin, _gpio_value)

    utils.logger.info("Callback of type " + _callback_type + " finished")


# ================# Functions #================ #
