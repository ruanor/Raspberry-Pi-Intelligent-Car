#-*- coding:UTF-8 -*-

import RPi.GPIO as GPIO
import time

#舵机引脚定义
ServoPin1 = 11
ServoPin2 = 9

#设置GPIO口为BCM编码方式

GPIO.setmode(GPIO.BCM)

#忽略警告信息

GPIO.setwarnings(False)

#舵机引脚设置为输出模式

def init():

    GPIO.setup(ServoPin1, GPIO.OUT)
    GPIO.setup(ServoPin2, GPIO.OUT)

#定义一个脉冲函数，用来模拟方式产生pwm值

#时基脉冲为20ms，该脉冲高电平部分在0.5-

#2.5ms控制0-180度

def servo_pulse1(myangle):
    pulsewidth = (myangle * 11) + 500
    GPIO.output(ServoPin1, GPIO.HIGH)
    time.sleep(pulsewidth/1000000.0)
    GPIO.output(ServoPin1, GPIO.LOW)
    time.sleep(20.0/1000-pulsewidth/1000000.0)

def servo_pulse2(myangle):
    pulsewidth = (myangle * 11) + 500
    GPIO.output(ServoPin2, GPIO.HIGH)
    time.sleep(pulsewidth/1000000.0)
    GPIO.output(ServoPin2, GPIO.LOW)
    time.sleep(20.0/1000-pulsewidth/1000000.0)

#舵机来回转动
def servo_control1():
    for pos in range(181):
        servo_pulse1(pos)
        #time.sleep(0.009)

    for pos in reversed(range(181)):
        servo_pulse1(pos)
        #time.sleep(0.009)

def servo_control2():
    for pos in range(45,135):
        servo_pulse2(pos)
        #time.sleep(0.009)

    for pos in reversed(range(45,135)):
        servo_pulse2(pos)
        #time.sleep(0.009)
        
#延时2s  

time.sleep(2)
try:

    init()
    while True:
        servo_control1()
        servo_control2()

except KeyboardInterrupt:

    pass