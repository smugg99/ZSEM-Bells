#ifndef DS1302_H
#define DS1302_H

static int bcdToD(unsigned int byte, unsigned int mask);

static unsigned int dToBcd(unsigned int byte);

static int ramTest(void);

static int setLinuxClock(void);

static void getDSclock(int* year, int* mon, int* mday, int* hour, int* min, int* sec);

static int setDSclock(int sec, int min, int hour, int mday, int mon, int wday, int year);

static void setup(const int clockPin, const int dataPin, const int csPin);


#endif