import RPi.GPIO as GPIO
import time

class Distance():

    ECHO = 27    #输入
    TRIG = 22   #输出

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Distance.ECHO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(Distance.TRIG, GPIO.OUT)

    def distance(self):
        GPIO.output(Distance.TRIG, GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(Distance.TRIG, GPIO.LOW)

        #等低电平结束，记录时间
        while GPIO.input(Distance.ECHO) == GPIO.LOW:
            pass
        t1 = time.time()

        #等高电平结束，记录时间
        while GPIO.input(Distance.ECHO) == GPIO.HIGH:
            pass
        t2 = time.time()

        #返回距离
        return (t2 - t1) * 36000 / 2

    def destroy(self):
        GPIO.cleanup()


if __name__ == '__main__':
    try:
        distance = Distance()
        distance.setup()
        while True:
            dis = distance.distance()
            print(dis)
            time.sleep(0.3)
    except KeyboardInterrupt:
        distance.destory()






