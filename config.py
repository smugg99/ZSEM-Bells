# ================# API #================ #

#SCHEDULE_URL = "https://zsem.edu.pl/plany/plany"
SCHEDULE_URL = "https://zsemm.edu.pl/plan/plany"

# Examples
# http://www.plan.lzk.pl/plany/o1.html
# https://zsem.edu.pl/plany/plany/o5.html
# https://zsemm.edu.pl/plan/plany/o1.html

SCHEDULE_BRANCH_ENDPOINT = "/o{}.html"
SCHEDULE_MAX_BAD_BRANCHES = 3

SCHEDULE_TABLE_CLASS_NAME = "tabela"

# SCHEDULE_TEACHER_ENDPOINT = "/n{teacher_index}.html"
# SCHEDULE_CLASSROOM_ENDPOINT = "/s{classroom_index}.html"

SCHEDULE_REQUEST_TIMEOUT = 5

TIME_API_URL = "http://worldtimeapi.org/api/ip"
TIME_API_REQUEST_TIMEOUT = 5

# ================# API #================ #


# ================# Logger #================ #

# LOGGER_MIN_FORMAT = "%(asctime)s - %(name)s - %(message)s"
# LOGGER_MED_FORMAT = "%(asctime)s - %(name)s - %(message)s (%(filename)s:%(lineno)d)"
# LOGGER_MAX_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

LOGGER_MIN_FORMAT = "[%(asctime)s] - %(message)s"
LOGGER_MED_FORMAT = "[%(asctime)s] - %(message)s (%(filename)s:%(lineno)d)"
LOGGER_MAX_FORMAT = "[%(asctime)s] - [%(levelname)s] - %(message)s (%(filename)s:%(lineno)d)"

# ================# Logger #================ #
