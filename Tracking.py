import RPi.GPIO as GPIO
import time
import math


class Tracking():
    CS = 5
    CLOCK = 25
    ADDRESS = 24
    DATAOUT = 23

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup((Tracking.CS, Tracking.CLOCK, Tracking.ADDRESS), GPIO.OUT)
        GPIO.setup(Tracking.DATAOUT, GPIO.IN, GPIO.PUD_UP)

    def tracking_detect(self):
        value = [0] * 6
        for j in range(0, 6):
            GPIO.output(Tracking.CS, GPIO.LOW)
            for i in range(0, 10):
                if(i < 4):
                    bit = (((j) >> (3 - i)) & 0x01)
                    GPIO.output(Tracking.ADDRESS, bit)

                value[j] <<= 1
                value[j] |= GPIO.input(Tracking.DATAOUT)
                GPIO.output(Tracking.CLOCK, GPIO.HIGH)
                GPIO.output(Tracking.CLOCK, GPIO.LOW)

            GPIO.output(Tracking.CS, GPIO.HIGH)
            time.sleep(0.0001)
        left = math.floor(value[1]/400) #如果为0，则为黑色
        right = math.floor(value[5]/400) #如果为0，则为黑色
        return left, right

    def destroy(self):
        GPIO.cleanup()