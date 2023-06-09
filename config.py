# ================# API #================ #

# SCHEDULE_URL = "https://zsem.edu.pl/plany/plany"
MAIN_SITE: str = "https://zsem.edu.pl"
SCHEDULE_URL: str = MAIN_SITE + "/plany/plany"

# Examples
# http://www.plan.lzk.pl/plany/o1.html
# https://zsem.edu.pl/plany/plany/o5.html
# https://zsemm.edu.pl/plan/plany/o1.html

SCHEDULE_BRANCH_ENDPOINT: str = "/o{}.html"
SCHEDULE_MAX_BAD_BRANCHES: int = 3

SCHEDULE_TABLE_CLASS_NAME: str = "tabela"
SCHEDULE_TABLE_HOUR_CLASS_NAME: str = "g"

SCHEDULE_TABLE_MIN_ROWS: int = 2

# SCHEDULE_TEACHER_ENDPOINT = "/n{teacher_index}.html"
# SCHEDULE_CLASSROOM_ENDPOINT = "/s{classroom_index}.html"

SCHEDULE_REQUEST_TIMEOUT: int = 5

TIME_API_URL: str = "http://worldtimeapi.org/api/ip"
TIME_API_REQUEST_TIMEOUT: int = 5

# ================# API #================ #


# ================# Logger #================ #

# LOGGER_MIN_FORMAT = "%(asctime)s - %(name)s - %(message)s"
# LOGGER_MED_FORMAT = "%(asctime)s - %(name)s - %(message)s (%(filename)s:%(lineno)d)"
# LOGGER_MAX_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

LOGGER_MIN_FORMAT: str = "[%(asctime)s] - %(message)s"
LOGGER_MED_FORMAT: str = "[%(asctime)s] - %(message)s (%(filename)s:%(lineno)d)"
LOGGER_MAX_FORMAT: str = "[%(asctime)s] - [%(levelname)s] - %(message)s (%(filename)s:%(lineno)d)"

# ================# Logger #================ #
