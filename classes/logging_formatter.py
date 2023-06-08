import logging

import config


# ================# Classes #================ #


class LoggingFormatter:
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    green = "\x1b[32m"
    blue = "\x1b[34m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: blue + config.LOGGER_MED_FORMAT + reset,
        logging.INFO: green + config.LOGGER_MIN_FORMAT + reset,
        logging.WARNING: yellow + config.LOGGER_MAX_FORMAT + reset,
        logging.ERROR: red + config.LOGGER_MAX_FORMAT + reset,
        logging.CRITICAL: bold_red + config.LOGGER_MAX_FORMAT + reset
    }

    def format(self, record) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%H:%M:%S")

        return formatter.format(record)


# ================# Classes #================ #
