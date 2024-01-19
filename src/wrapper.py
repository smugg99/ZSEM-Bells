import asyncio
import os
# import pygame

from typing import Dict, Optional, List
from asyncio.subprocess import Process

import OPi.GPIO as GPIO
import utils
import config

from enum import Enum

callback_pins_enabled: Optional[bool] = utils.user_config.get("callback_pins_enabled", False)
status_pins_enabled: Optional[bool] = utils.user_config.get("status_pins_enabled", False)
gpio_pins_config: Optional[Dict[str, int]] = utils.user_config.get("gpio_pins", {})
skip_weekends: Optional[bool] = utils.user_config.get("skip_weekends", False)

_outputs_config: Optional[Dict[str, int]] = gpio_pins_config.get("outputs", {})
callback_pins: Dict[str, int] = [
    _outputs_config["work_callback"],
    _outputs_config["break_callback"],
    _outputs_config["neutral_callback"]
]


class StatusLed(Enum):
    SUCCESS = _outputs_config["success_led"]
    WARNING = _outputs_config["warning_led"]
    ERROR = _outputs_config["error_led"]
    INTERNET_ACCESS = _outputs_config["internet_access_led"]
    API_ACCESS = _outputs_config["api_access_led"]


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
        await asyncio.wait_for(process.wait(), timeout=config.MAX_SIGNAL_DURATION)

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

# async def _play_wav_async(wav_filename: str):
#     try:
#         # Get the project root directory
#         project_root: str = os.path.abspath(os.path.join(
#             os.path.dirname(os.path.abspath(__file__)), ".."))

#         # Construct the path to the WAV file based on the config_dir and sound_filename
#         wav_file_path: str = os.path.join(
#             project_root, config.SOUNDS_FOLDER_PATH, wav_filename)
        
#         pygame.mixer.init()
#         print(wav_file_path)
#         pygame.mixer.music.load(wav_file_path)
#         pygame.mixer.music.play()
        
#         await asyncio.sleep(config.MAX_SIGNAL_DURATION)
        
#         pygame.mixer.quit()
#     except Exception as e:
#         print(e)
#         raise(e)


# Note: This should actually be called setup callback pins or something
def setup_gpio_pins() -> bool:
    utils.logging_formatter.separator("Setting up GPIO")

    if callback_pins_enabled:
        # gpio_pins_config: Optional[Dict[str, int]
        #                            ] = utils.user_config.get("gpio_pins", {})

        # _outputs_config: Optional[Dict[str, int]
        #                           ] = gpio_pins_config.get("outputs", {})

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

            for pin in _outputs_config.values():
                try:
                    GPIO.setup(pin, GPIO.OUT)
                except Exception as e:
                    print(e)
                    return False
                else:
                    utils.logger.log("Setting gpio " + str(pin) + " as OUTPUT")
                    if pin in callback_pins:
                        GPIO.output(pin, GPIO.HIGH)
                    else:
                        GPIO.output(pin, GPIO.LOW)

        return True
    else:
        utils.logger.warn("GPIOs are disabled")
        return False


def cleanup_gpio():
    if callback_pins_enabled:
        utils.logging_formatter.separator("Cleaning up GPIO")
        GPIO.cleanup()

def toggle_status_led(status_led: StatusLed, value: bool = True):
    if not status_pins_enabled:
        return
    
    alone_group: list[StatusLed] = [StatusLed.SUCCESS, StatusLed.WARNING, StatusLed.ERROR]
    
    if status_led not in alone_group:
        GPIO.output(status_led.value, value)
        return
        
    for led in alone_group:
        if led == status_led:
            GPIO.output(led.value, value)
        else:
            GPIO.output(led.value, False)

async def callback_handler(is_work: bool, is_weekend: bool, gpio_setup_good: bool):
    outputs: Optional[Dict[str, int]] = gpio_pins_config.get("outputs", {})

    _callback_type: str = ("work" if is_work else "break")
    _gpio_good: bool = False

    if is_weekend and skip_weekends:
        utils.logger.info("Skipping callback, it's the weekend!")
        return

    if callback_pins_enabled and gpio_setup_good:
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
                _gpio_value: bool = GPIO.LOW

                utils.logger.log("GPIO " + str(gpio_pin) + " is ON!")
                GPIO.output(gpio_pin, _gpio_value)
                GPIO.output(neutral_gpio_pin, _gpio_value)

    if utils.user_config["sounds_enabled"]:
        _bell_sound_filename: str = utils.user_config["bell_sounds"][_callback_type]
        utils.logger.info("Sound should be playing right now!")
        await play_wav_async(_bell_sound_filename)
    else:
        utils.logger.info("Delay should be performed right now!")
        await asyncio.sleep(config.MAX_SIGNAL_DURATION)

    if _gpio_good and gpio_setup_good:
        _gpio_value: bool = GPIO.HIGH

        utils.logger.log("GPIO " + str(gpio_pin) + " is OFF!")
        GPIO.output(gpio_pin, _gpio_value)
        GPIO.output(neutral_gpio_pin, _gpio_value)

    utils.logger.info("Callback of type " + _callback_type + " finished")


def handle_error(exception):
    print(f"Error occurred: {exception}")

    for status_led in StatusLed:
        toggle_status_led(status_led, False)

    toggle_status_led(StatusLed.ERROR, True)
    # cleanup_gpio()

# ================# Functions #================ #
