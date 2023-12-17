from python.DS1302 import setup, get_clock
from datetime import datetime

setup(clock_pin=7, data_pin=5, cs_pin=8)
print(setup)

year, mon, mday, hour, min, sec = get_clock()
ds_datetime = datetime(year, mon, mday, hour, min, sec)

print("DS1302 Clock:", ds_datetime)