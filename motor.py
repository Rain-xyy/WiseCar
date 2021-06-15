import RPi.GPIO as GPIO



class Motor():

    A1 = 13
    B1 = 12
    CONTROL1 = 6
    A2 = 21
    B2 = 20
    CONTROL2 = 26

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup((Motor.A1, Motor.B1, Motor.CONTROL1), GPIO.OUT)
        GPIO.setup((Motor.A2, Motor.B2, Motor.CONTROL2), GPIO.OUT)


    def pwm(self, pwm):
        pwm = GPIO.PWM(pwm, 1000)
        pwm.start(0)  #初始占空比为0
        return pwm    #返回pwm对象

    def changeSpeed(self, pwm, speed):
        pwm.ChangeDutyCycle(speed) #改变占空比

    def clockwise(self, A, B): #顺时针
        GPIO.output((A, B), (1, 0))

    def counterClockwise(self, A, B): #逆时针
        GPIO.output((A, B), (0, 1))

    def stop(self, A, B):
        GPIO.output((A, B), (0, 0))


    def destroy(self, pwm1, pwm2):
        pwm1.stop()
        pwm2.stop()
        GPIO.cleanup()

#if __name__=="__main__":
