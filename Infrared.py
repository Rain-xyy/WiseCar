import RPi.GPIO as GPIO
import time


class Infrared():
    InfraredLeft = 16
    InfraredRight = 19

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Infrared.InfraredLeft, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(Infrared.InfraredRight, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def infra_detect(self):
        infra_left_value = 1
        infra_right_value = 1
        if (GPIO.input(Infrared.InfraredLeft) == 0):  # 左侧有障碍物，输出低电平
            infra_left_value = 0
        if (GPIO.input(Infrared.InfraredRight)):  # 右侧有障碍物，输出低电平
            infra_right_value = 0
        return infra_left_value, infra_right_value

    def destroy(self):
        GPIO.cleanup()
