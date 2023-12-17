from ctypes import CDLL, c_int

libwiringPiDev = CDLL('./build/DS1302.so')
# libwiringPiDev = CDLL('/usr/local/lib/libwiringPiDev.so')

libwiringPiDev.ds1302setup.argtypes = [c_int, c_int, c_int]
libwiringPiDev.ds1302clockRead.argtypes = [c_int * 8]
libwiringPiDev.ds1302clockWrite.argtypes = [c_int * 8]

def setup(clock_pin, data_pin, cs_pin):
    libwiringPiDev.ds1302setup(clock_pin, data_pin, cs_pin)


def get_clock():
    from ctypes import byref

    sec = c_int()
    min = c_int()
    hour = c_int()
    mday = c_int()
    mon = c_int()
    wday = c_int()
    year = c_int()

    libwiringPiDev.ds1302clockRead(byref(sec), byref(min), byref(
        hour), byref(mday), byref(mon), byref(wday), byref(year))

    return sec.value, min.value, hour.value, mday.value, mon.value, wday.value, year.value


def set_clock(sec, min, hour, mday, mon, wday, year):
    libwiringPiDev.ds1302clockWrite(sec, min, hour, mday, mon, wday, year)

# def set_linux_clock():
#     ds1302_lib.setLinuxClock()

# def ram_test():
#     ds1302_lib.ramTest()