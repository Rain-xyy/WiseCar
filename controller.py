#对小车进行控制

class Controller():

    def __init__(self, car, pwm1, pwm2):
        self.car = car
        self.pwm1 = pwm1
        self.pwm2 = pwm2
        self.acc_value = 25

    def accelerator(self, left_speed = 1, right_speed = 1):
        self.car.changeSpeed(self.pwm1, self.acc_value * left_speed * 0.85)
        self.car.changeSpeed(self.pwm2, self.acc_value * right_speed)

    def turnLeft(self):
        #左转弯
        self.car.counterClockwise(self.car.A1, self.car.B1) #左车轮后退
        self.car.clockwise(self.car.A2, self.car.B2) #右车轮前进

    def turnRight(self):
        #右转弯
        self.car.clockwise(self.car.A1, self.car.B1)  # 左车轮前进
        self.car.counterClockwise(self.car.A2, self.car.B2)  # 右车轮后退

    def forward(self):
        #前进
        self.car.clockwise(self.car.A1, self.car.B1)  # 左车轮前进
        self.car.clockwise(self.car.A2, self.car.B2)  # 右车轮前进

    def backword(self):
        #后退
        self.car.counterClockwise(self.car.A1, self.car.B1)  # 左车轮后退
        self.car.counterClockwise(self.car.A2, self.car.B2)  # 右车轮后退

    def stop(self):
        #停止
        self.car.stop(self.car.A1, self.car.B1)
        self.car.stop(self.car.A2, self.car.B2)





