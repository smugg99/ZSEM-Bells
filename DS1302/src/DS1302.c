/*
 * ds1302.c:
 *	Real Time clock
 *
 * Copyright (c) 2013 Gordon Henderson.
 ***********************************************************************
 * This file is part of wiringPi:
 *	https://projects.drogon.net/raspberry-pi/wiringpi/
 *
 *    wiringPi is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU Lesser General Public License as published by
 *    the Free Software Foundation, either version 3 of the License, or
 *    (at your option) any later version.
 *
 *    wiringPi is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU Lesser General Public License for more details.
 *
 *    You should have received a copy of the GNU Lesser General Public License
 *    along with wiringPi.  If not, see <http://www.gnu.org/licenses/>.
 ***********************************************************************
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <wiringPi.h>
#include <ds1302.h>

 // Register defines

#define RTC_SECS 0
#define RTC_MINS 1
#define RTC_HOURS 2
#define RTC_DATE 3
#define RTC_MONTH 4
#define RTC_DAY 5
#define RTC_YEAR 6
#define RTC_WP 7
#define RTC_TC 8
#define RTC_BM 31

static unsigned int masks[] = {
    0x7F,
    0x7F,
    0x3F,
    0x3F,
    0x1F,
    0x07,
    0xFF
};

/*
 * bcdToD: dToBCD:
 *	BCD decode/encode
 *********************************************************************************
 */

static int bcdToD(unsigned int byte, unsigned int mask) {
    unsigned int b1, b2;
    byte &= mask;
    b1 = byte & 0x0F;
    b2 = ((byte >> 4) & 0x0F) * 10;
    return b1 + b2;
}

static unsigned int dToBcd(unsigned int byte) {
    return ((byte / 10) << 4) + (byte % 10);
}

/*
 * ramTest:
 *	Simple test of the 31 bytes of RAM inside the DS1302 chip
 *********************************************************************************
 */

static int ramTestValues[] = {
    0x00,
    0xFF,
    0xAA,
    0x55,
    0x01,
    0x02,
    0x04,
    0x08,
    0x10,
    0x20,
    0x40,
    0x80,
    0x00,
    0xF0,
    0x0F,
    -1
};

static int ramTest(void) {
    int addr;
    int got;
    int i = 0;
    int errors = 0;
    int testVal;

    printf("DS1302 RAM TEST\n");

    testVal = ramTestValues[i];

    while (testVal != -1) {
        for (addr = 0; addr < 31; ++addr)
            ds1302ramWrite(addr, testVal);

        for (addr = 0; addr < 31; ++addr)
            if ((got = ds1302ramRead(addr)) != testVal) {
                printf("DS1302 RAM Failure: Address: %2d, Expected: 0x%02X, Got: 0x%02X\n",
                    addr, testVal, got);
                ++errors;
            }
        testVal = ramTestValues[++i];
    }

    for (addr = 0; addr < 31; ++addr)
        ds1302ramWrite(addr, addr);

    for (addr = 0; addr < 31; ++addr)
        if ((got = ds1302ramRead(addr)) != addr) {
            printf("DS1302 RAM Failure: Address: %2d, Expected: 0x%02X, Got: 0x%02X\n",
                addr, addr, got);
            ++errors;
        }

    if (errors == 0)
        printf("-- DS1302 RAM TEST: OK\n");
    else
        printf("-- DS1302 RAM TEST FAILURE. %d errors.\n", errors);

    return 0;
}

/*
 * setLinuxClock:
 *	Set the Linux clock from the hardware
 *********************************************************************************
 */

static int setLinuxClock(void) {
    char dateTime[20];
    char command[64];
    int clock[8];

    printf("Setting the Linux Clock from the DS1302... ");
    fflush(stdout);

    ds1302clockRead(clock);

    // [MMDDhhmm[[CC]YY][.ss]]

    sprintf(dateTime, "%02d%02d%02d%02d%02d%02d.%02d",
        bcdToD(clock[RTC_MONTH], masks[RTC_MONTH]),
        bcdToD(clock[RTC_DATE], masks[RTC_DATE]),
        bcdToD(clock[RTC_HOURS], masks[RTC_HOURS]),
        bcdToD(clock[RTC_MINS], masks[RTC_MINS]),
        20,
        bcdToD(clock[RTC_YEAR], masks[RTC_YEAR]),
        bcdToD(clock[RTC_SECS], masks[RTC_SECS]));

    sprintf(command, "/bin/date %s", dateTime);
    system(command);

    return 0;
}

/*
 * getDSclock:
 *	Get the DS1302 time
 *********************************************************************************
 */
void getDSclock(int* year, int* mon, int* mday, int* hour, int* min, int* sec) {
    int clock[8];
    ds1302clockRead(clock);

    *year = bcdToD(clock[RTC_YEAR], masks[RTC_YEAR]) + 2000;
    *mon = bcdToD(clock[RTC_MONTH], masks[RTC_MONTH]);
    *mday = bcdToD(clock[RTC_DATE], masks[RTC_DATE]);
    *hour = bcdToD(clock[RTC_HOURS], masks[RTC_HOURS]);
    *min = bcdToD(clock[RTC_MINS], masks[RTC_MINS]);
    *sec = bcdToD(clock[RTC_SECS], masks[RTC_SECS]);
}

/*
 * setDSclock:
 *	Set the DS1302 block from Linux time
 *********************************************************************************
 */

int setDSclock(int sec, int min, int hour, int mday, int mon, int wday, int year) {
    int clock[8];

    printf("Setting the clock in the DS1302 from given time... ");

    clock[0] = dToBcd(sec); // seconds
    clock[1] = dToBcd(min); // mins
    clock[2] = dToBcd(hour); // hours
    clock[3] = dToBcd(mday); // date
    clock[4] = dToBcd(mon + 1); // months 0-11 --> 1-12
    clock[5] = dToBcd(wday + 1); // weekdays (sun 0)
    clock[6] = dToBcd(year - 100); // years
    clock[7] = 0; // W-Protect off

    ds1302clockWrite(clock);

    printf("OK\n");

    return 0;
}

void setup(const int clockPin, const int dataPin, const int csPin) {
    printf("Setup\n");
    wiringPiSetupGpio();

    printf(clockPin, dataPin, csPin);
    ds1302setup(clockPin, dataPin, csPin);
}