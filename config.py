from datetime import datetime

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

# ================# API #================ #


# ================# Scraper #================ #

SCHEDULE_MAX_BAD_BRANCHES: int = 3

SCHEDULE_TABLE_CLASS_NAME: str = "tabela"
SCHEDULE_TABLE_HOUR_CLASS_NAME: str = "g"

SCHEDULE_TABLE_MIN_ROWS: int = 2

SCHEDULE_FILE_PATH: str = "schedule.json"

# ================# Scraper #================ #


# ================# Logger #================ #

# LOGGER_MIN_FORMAT = "%(asctime)s - %(name)s - %(message)s"
# LOGGER_MED_FORMAT = "%(asctime)s - %(name)s - %(message)s (%(filename)s:%(lineno)d)"
# LOGGER_MAX_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

LOGS_FILE_PATH: str = "last_logs.txt"

LOGGER_LOG_FORMAT: str = "%(message)s - (%(filename)s:%(lineno)d) - [%(asctime)s]"
LOGGER_RAW_FORMAT: str = "%(message)s"

LOGGER_RAW_LEVEL: int = 25
LOGGER_LOG_LEVEL: int = 24

LOGGER_MIN_FORMAT: str = "[%(asctime)s] - %(message)s"
LOGGER_MED_FORMAT: str = "[%(asctime)s] - %(message)s (%(filename)s:%(lineno)d)"
LOGGER_MAX_FORMAT: str = "[%(asctime)s] - [%(levelname)s] - %(message)s (%(filename)s:%(lineno)d)"

# ================# Logger #================ #

USER_CONFIG_FILE_PATH: str = "user_config.json"
CLOCK_RUNNING_ANNOUNCE_INTERVAL: int = 60