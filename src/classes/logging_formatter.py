from datetime import datetime
import logging

import config
import utils

# ================# Classes #================ #


class LoggingFormatter:
    cyan = "\x1b[36m"
    magenta = "\x1b[35m"
    white = "\x1b[37m"
    bright_yellow = "\x1b[33;1m"
    bright_green = "\x1b[32;1m"
    bright_blue = "\x1b[34;1m"
    bright_cyan = "\x1b[36;1m"
    bright_magenta = "\x1b[35;1m"
    bright_white = "\x1b[37;1m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    green = "\x1b[32m"
    blue = "\x1b[34m"
    bold_red = "\x1b[31;1m"
    underline = "\x1b[4m"
    reset = "\x1b[0m"

    FORMATS = {
        # 25 is between INFO level and WARNING level, it stands for the RAW level
        25: white + config.LOGGER_RAW_FORMAT + reset,
        24: cyan + config.LOGGER_LOG_FORMAT + reset,
        logging.DEBUG: blue + config.LOGGER_MED_FORMAT + reset,
        logging.INFO: green + config.LOGGER_MIN_FORMAT + reset,
        logging.WARNING: yellow + config.LOGGER_MAX_FORMAT + reset,
        logging.ERROR: red + config.LOGGER_MAX_FORMAT + reset,
        logging.CRITICAL: bold_red + config.LOGGER_MAX_FORMAT + reset
    }

    def __init__(self):
        # Can't choose between them yet...
        self.raw_formatter = logging.Formatter(
            config.LOGGER_RAW_FORMAT, datefmt="%H:%M:%S")
        self.log_formatter = logging.Formatter(
            config.LOGGER_LOG_FORMAT, datefmt="%H:%M:%S")

    def format(self, record) -> str:
        log_fmt: str = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%H:%M:%S")

        return formatter.format(record)

    def startup(self):
        self.separator("Program Startup")
        utils.logger.raw(str(datetime.now()))

    def separator(self, text: str):
        utils.logger.raw(
            "# ================# {} #================ #".format(text))

    def test(self):
        self.separator("Logger Test")

        utils.logger.log("log message test")
        utils.logger.raw("raw message test")
        utils.logger.debug("debug message test")
        utils.logger.info("info message test")
        utils.logger.warning("warning message test")
        utils.logger.error("error message test")
        utils.logger.critical("critical message test")

# ================# Classes #================ #
