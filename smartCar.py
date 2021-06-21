import random

from motor import Motor
from controller import Controller
from Distance import Distance
from Infrared import Infrared
from Tracking import Tracking
import time
import threading
from LED import LED
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

smp_car = Motor() #初始化电机
smp_car.setup()

pwm1 = smp_car.pwm(smp_car.CONTROL1) #初始化左边车轮控制
pwm2 = smp_car.pwm(smp_car.CONTROL2) #初始化右边车轮控制

smart_car = Controller(smp_car, pwm1, pwm2)

ultr = Distance() #初始化超声波测距
ultr.setup()    #初始化引脚

infrared = Infrared() #初始化红外避障
infrared.setup()  #初始化引脚

tracking = Tracking() #初始化循迹
tracking.setup()  #初始化引脚

exit_ultra = 1
def ultra_control():
    while True:
        while not exit_ultra:
            smart_car.acc_value = 20
            smart_car.accelerator()

            dis = ultr.distance()
            if(dis < 10): #后退0.3s
                smart_car.backword()
            elif(dis < 20):
                infra_left_value, infra_right_value = infrared.infra_detect()
                # print(infra_left_value, " ", infra_right_value)

                # 红外避障控制
                if infra_left_value == 0:  # 左侧有障碍物
                    smart_car.turnRight()

                if infra_right_value == 0:  # 右侧有障碍物
                    smart_car.turnLeft()
                else:                       #随即向左或向右偏移
                    val = random.random()
                    if val > 0.5:
                        smart_car.turnRight()
                    else:
                        smart_car.turnLeft()
            else:
                smart_car.forward()

            time.sleep(0.3)


# def infra_control():
#     smart_car.accelerator(0.5, 0.5)
#     infra_left_value, infra_right_value = infrared.infra_detect()
#     #print(infra_left_value, " ", infra_right_value)
#
#     #红外避障控制
#     if infra_left_value == 0:   #左侧有障碍物
#         smart_car.turnRight()
#         time.sleep(0.5)  # 右转0.5s
#         smart_car.stop()
#
#
#     if infra_right_value == 1: #右侧有障碍物
#         smart_car.turnLeft()
#         time.sleep(0.5)  #左转0.5s
#         smart_car.stop()

exit_tracking = 1 #是否退出小车循迹的while循环的标志，为0则不退出循迹
def trackibg_control():
    #红外传感器，控制小车沿黑线自动行进
    while True:
        time.sleep(0.1)
        while not exit_tracking:
            smart_car.acc_value = 30 #占空比的基值为10
            tracking_left_value, tracking_right_value = tracking.tracking_detect()
            #print(tracking_left_value, " ", tracking_right_value)
            if tracking_left_value == 0 and tracking_right_value == 0: #左右都没有检测到红外反射，停车
                smart_car.stop()

            if tracking_left_value == 1 and tracking_right_value == 0: #右侧没有检测到红外反射，即遇到黑线，右转
                smart_car.accelerator(1, 0)
                smart_car.forward()

            if tracking_left_value == 0 and tracking_right_value == 1: #左侧没有检测到反射信号，即遇到黑线，左转
                smart_car.accelerator(0, 1)
                smart_car.forward()

            if tracking_left_value == 1 and tracking_right_value == 1: #左右都能检测到红外反射，前进
                smart_car.accelerator() #左右车速一致
                smart_car.forward()



if __name__ == "__main__":
    try:
        #创建循迹控制线程
        thread_tracking = threading.Thread(target=trackibg_control)
        thread_tracking.start()

        #创建自动避障线程
        thread_distance = threading.Thread(target=ultra_control)
        thread_distance.start()

        f = open("/dev/input/event0", "rb")
        while True:
            d = f.read(48)
            key = d.hex()[40:42]
            print(key)
            if key == "45": #按下该按键，进入循迹模式
                exit_tracking = 0 #由循迹线程控制小车前进
                exit_ultra = 1
            elif key == "46":
                exit_ultra = 0  #有自动避障功能控制小车前进
                exit_tracking = 1
            else:
                exit_tracking = 1 #结束循迹线程中的while循环
                exit_ultra = 1    #结束自动避障中的while循环

                smart_car.accelerator()
                if key == "08":
                    smart_car.turnLeft()
                elif key == "5a":
                    smart_car.turnRight()
                elif key == "18":
                    smart_car.forward()
                elif key == "52":
                    smart_car.backword()
                elif key == "0c":
                    if(smart_car.acc_value < 80):
                        smart_car.acc_value += 20
                    smart_car.accelerator()
                elif key == "5e":
                    if(smart_car.acc_value > 20):
                        smart_car.acc_value -= 20
                    smart_car.accelerator()
                elif key == "1c":
                    smart_car.accelerator(0, 0)
                elif key == "42":
                    LED()
                elif key == "4a":
                    break
    except KeyboardInterrupt:
        smp_car.destroy(pwm1, pwm2)
    finally:
        smp_car.destroy(pwm1, pwm2)




















