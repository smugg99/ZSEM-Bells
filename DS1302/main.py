from python.DS1302 import setup, get_clock
print("balls")
from datetime import datetime

setup(clock_pin=7, data_pin=5, cs_pin=8)
print("balls")

year, mon, mday, hour, min, sec, deez = get_clock()
print(year, mon, mday, hour, min, sec, deez)
ds_datetime = datetime(year, mon, mday, hour, min, sec, deez)
print("balls")
print("DS1302 Clock:", ds_datetime)