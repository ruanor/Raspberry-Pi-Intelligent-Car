#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time

#小车按键定义
key = 8

#RGB三色灯引脚定义
LED_R = 22
LED_G = 27
LED_B = 24

#红外避障引脚定义
AvoidSensorLeft = 12
AvoidSensorRight = 17

#设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BCM)

#忽略警告信息
GPIO.setwarnings(False)

#电机引脚初始化为输出模式
#按键引脚初始化为输入模式
#红外避障引脚初始化为输入模式
def init():
    GPIO.setup(AvoidSensorLeft,GPIO.IN)
    GPIO.setup(AvoidSensorRight,GPIO.IN)
    GPIO.setup(LED_R, GPIO.OUT)
    GPIO.setup(LED_G, GPIO.OUT)
    GPIO.setup(LED_B, GPIO.OUT)
    GPIO.setup(key,GPIO.IN)
    
  

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
    while True:
        #遇到障碍物,红外避障模块的指示灯亮,端口电平为LOW
        #未遇到障碍物,红外避障模块的指示灯灭,端口电平为HIGH
        LeftSensorValue  = GPIO.input(AvoidSensorLeft);
        RightSensorValue = GPIO.input(AvoidSensorRight);

        if LeftSensorValue == True and RightSensorValue == True :
            GPIO.output(LED_R, GPIO.HIGH)
            GPIO.output(LED_G, GPIO.LOW)
            GPIO.output(LED_B, GPIO.LOW)
            time.sleep(0.5)
        elif LeftSensorValue == True and RightSensorValue == False :
            GPIO.output(LED_R, GPIO.LOW)
            GPIO.output(LED_G, GPIO.HIGH)
            GPIO.output(LED_B, GPIO.LOW)
            time.sleep(0.5)
        elif RightSensorValue == True and LeftSensorValue == False:
            GPIO.output(LED_R, GPIO.LOW)
            GPIO.output(LED_G, GPIO.LOW)
            GPIO.output(LED_B, GPIO.HIGH)
            time.sleep(0.5)
        elif RightSensorValue == False and LeftSensorValue == False :
            GPIO.output(LED_R, GPIO.LOW)
            GPIO.output(LED_G, GPIO.LOW)
            GPIO.output(LED_B, GPIO.LOW)
            time.sleep(0.5)
except KeyboardInterrupt:
    pass
GPIO.cleanup()