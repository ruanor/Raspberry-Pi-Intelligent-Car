# -*- coding:UTF-8 -*-

import RPi.GPIO as GPIO
import time

#RGB三色灯引脚定义
sound=8

#设置RGB三色灯为BCM编码方式
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#RGB三色灯设置为输出模式
GPIO.setup(sound, GPIO.OUT)

#循环显示7种不同的颜色s
try:
    while True:
        GPIO.output(sound,GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(sound,GPIO.HIGH)
        time.sleep(0.5)

except:
    print "except"
#使用try except语句，当CTRL+C结束进程时会触发异常后
#会执行gpio.cleanup()语句清除GPIO管脚的状态
GPIO.cleanup()