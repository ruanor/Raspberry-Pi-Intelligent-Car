#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time

#小车电机引脚定义
MOTOR=2

#小车按键定义
key = 8


#设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BCM)

#忽略警告信息
GPIO.setwarnings(False)

#电机引脚初始化为输出模式
#按键引脚初始化为输入模式
#红外避障引脚初始化为输入模式
def init():
    global pwm
    GPIO.setup(MOTOR,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(key,GPIO.IN)
    pwm = GPIO.PWM(MOTOR, 1)
    pwm.start(0)
	
#小车前进	
def run(value):
    #GPIO.output(MOTOR, GPIO.HIGH)
    pwm.ChangeDutyCycle(value)

#小车停止	
def brake():
   #GPIO.output(MOTOR, GPIO.LOW)
    pwm.stop()

#按键检测
def key_scan():
    while GPIO.input(key):
         pass
    while not GPIO.input(key):
         time.sleep(0.01)
         if not GPIO.input(key):
             time.sleep(0.01)
	     while not GPIO.input(key):
	         pass

#延时2s	
time.sleep(2)

#try/except语句用来检测try语句块中的错误，
#从而让except语句捕获异常信息并处理。
try:
    init()
    key_scan()
    run(80)
    time.sleep(3)
    run(60)
    time.sleep(3)
    run(40)
    time.sleep(3)
    run(20)
    time.sleep(3)
    brake()
        
       
except KeyboardInterrupt:
    pass
GPIO.cleanup()