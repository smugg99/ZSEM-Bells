import logging
from classes.logging_formatter import LoggingFormatter

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(LoggingFormatter())

logger.addHandler(stream_handler)
