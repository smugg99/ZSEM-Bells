from ctypes import CDLL, c_int

ds1302_lib = CDLL('./build/DS1302.so')

ds1302_lib.ds1302setup.argtypes = [c_int, c_int, c_int]
ds1302_lib.ds1302clockRead.argtypes = [c_int * 8]
ds1302_lib.ds1302clockWrite.argtypes = [c_int * 8]
ds1302_lib.setDSclock.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int, c_int]


def setup(clock_pin, data_pin, cs_pin):
    ds1302_lib.setup(clock_pin, data_pin, cs_pin)

def get_clock():
    year, mon, mday, hour, min, sec = c_int(), c_int(), c_int(), c_int(), c_int(), c_int()
    ds1302_lib.getDSclock(year, mon, mday, hour, min, sec)

    return year.value, mon.value, mday.value, hour.value, min.value, sec.value


def set_clock(sec, min, hour, mday, mon, wday, year):
    ds1302_lib.ds1302clockWrite(sec, min, hour, mday, mon, wday, year)

def set_ds_clock(sec, min, hour, mday, mon, wday, year):
    ds1302_lib.setDSclock(sec, min, hour, mday, mon, wday, year)

def set_linux_clock():
    ds1302_lib.setLinuxClock()

def ram_test():
    ds1302_lib.ramTest()