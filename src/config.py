"""
config.py

This Python script defines various configuration settings for the application. It includes settings
related to API endpoints, scraper parameters, logging formats, runner information,
and miscellaneous options. Modify these settings to customize the behavior of the application.

Configuration Sections:
- API: Settings related to external APIs and web endpoints.
- Scraper: Parameters for web scraping and data extraction.
- Logger: Logging format and levels for application logs.
- Runner: Information about the application, author, and version.
- Misc: Miscellaneous settings, including user configuration file paths, audio settings, and other options.

"""


from typing import Dict


# ================# API #================ #

# Examples
# http://www.plan.lzk.pl/plany/o1.html
# https://zsem.edu.pl/plany/plany/o5.html
# https://zsemm.edu.pl/plan/plany/o1.html

MAIN_SITE: str = "https://zsem.edu.pl"
SCHEDULE_URL: str = MAIN_SITE + "/plany/plany"

SCHEDULE_BRANCH_ENDPOINT: str = "/o{}.html"
SCHEDULE_REQUEST_TIMEOUT: int = 5

SYNC_INTERVAL: int = 5

TIME_API_URL: str = "http://worldtimeapi.org/api/ip"
TIME_API_REQUEST_TIMEOUT: int = 5

STATUS_REQUEST_TIMEOUT: int = 5

# ================# API #================ #


# ================# Scraper #================ #

SCHEDULE_MAX_BAD_BRANCHES: int = 3

SCHEDULE_TABLE_CLASS_NAME: str = "tabela"
SCHEDULE_TABLE_HOUR_CLASS_NAME: str = "g"

SCHEDULE_TABLE_MIN_ROWS: int = 2

SCHEDULE_FILE_PATH: str = "data/schedule.json"

# ================# Scraper #================ #


# ================# Logger #================ #

# LOGGER_MIN_FORMAT = "%(asctime)s - %(name)s - %(message)s"
# LOGGER_MED_FORMAT = "%(asctime)s - %(name)s - %(message)s (%(filename)s:%(lineno)d)"
# LOGGER_MAX_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

LOGS_FILE_PATH: str = "data/last_logs.txt"

LOGGER_LOG_FORMAT: str = "%(message)s - (%(filename)s:%(lineno)d) - [%(asctime)s]"
LOGGER_RAW_FORMAT: str = "%(message)s"

LOGGER_RAW_LEVEL: int = 25
LOGGER_LOG_LEVEL: int = 24

LOGGER_MIN_FORMAT: str = "[%(asctime)s] - %(message)s"
LOGGER_MED_FORMAT: str = "[%(asctime)s] - %(message)s (%(filename)s:%(lineno)d)"
LOGGER_MAX_FORMAT: str = "[%(asctime)s] - [%(levelname)s] - %(message)s (%(filename)s:%(lineno)d)"

# ================# Logger #================ #


# ================# Runner #================ #

REPO_LINK: str = "https://github.com/SmeggMann99/ZSEM-Bells"
AUTHOR_NAME: str = "SmeggMann99"
VERSION: str = "1.0"

LANGS_FOLDER_PATH: str = "langs"
LANGUAGE_BINDINGS: Dict[str, str] = {
    "en": "en_US.UTF-8",
    "pl": "pl_PL.UTF-8"
}

# ================# Runner #================ #


# ================# Misc #================ #

USER_CONFIG_FILE_PATH: str = "data/user_config.json"
CLOCK_RUNNING_ANNOUNCE_INTERVAL: int = 60

DEFAULT_AUDIO_DEVICE: str = "hw:0,0"
MAX_SOUND_DURATION: int = 5
SOUNDS_FOLDER_PATH: str = "sounds"

MAX_BELL_DURATION: int = 5

INVERT_RELAY: bool = True

# ================# Misc #================ #
