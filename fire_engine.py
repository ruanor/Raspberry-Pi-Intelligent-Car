#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time
import smtplib #邮箱服务器smtp模块

import threading
import inspect
import ctypes

import enum
import cv2
import numpy as np

#自己的qq邮箱
QQMAIL_USER = '1428179843@qq.com'
#smtp服务的授权码
QQMAIL_PASS = 'cwfcylbuemrlhjeb'
#smtp的服务类型
SMTP_SERVER = 'smtp.qq.com'
#端口
SMTP_PORT = 25
#接受者，我这里是我自己
recipient1='1428179843@qq.com'
#邮件主题
sub1 = '灭火警示'
#邮件内容
text1='已发现火源'

#小车电机引脚定义
IN1 = 20   #AIN2
IN2 = 21   #AIN1
IN3 = 19   #BIN2
IN4 = 26   #BIN1
ENA = 16   #PWMA
ENB = 13   #PWMB

#小车风扇引脚定义
MOTOR=2

#摄像头舵机引脚定义
ServoPin1 = 11
ServoPin2 = 9

#RGB三色灯引脚定义
LED_R = 22
LED_G = 27
LED_B = 24

#小车按键定义
key = 8

#超声波引脚定义
EchoPin = 0
TrigPin = 1

#循迹红外引脚定义
#TrackSensorLeftPin1 TrackSensorLeftPin2 TrackSensorRightPin1 TrackSensorRightPin2
#      3                 5                  4                   18
TrackSensorLeftPin1  =  3   #定义左边第一个循迹红外传感器引脚为3口
TrackSensorLeftPin2  =  5   #定义左边第二个循迹红外传感器引脚为5口
TrackSensorRightPin1 =  4   #定义右边第一个循迹红外传感器引脚为4口
TrackSensorRightPin2 =  18  #定义右边第二个循迹红外传感器引脚为18口

#设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BCM)

#忽略警告信息
GPIO.setwarnings(False)

#电机引脚初始化为输出模式
#LED灯引脚初始化为输出模式
#按键引脚初始化为输入模式
#寻迹引脚初始化为输入模式
def init():
    global pwm_ENA
    global pwm_ENB
    global pwm_FAN
    GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(LED_R, GPIO.OUT)
    GPIO.setup(LED_G, GPIO.OUT)
    GPIO.setup(LED_B, GPIO.OUT)
    GPIO.setup(key,GPIO.IN)
    GPIO.setup(EchoPin,GPIO.IN)  #超声波接收引脚为输入模式
    GPIO.setup(TrigPin,GPIO.OUT)  #超声波发送引脚为输出模式
    GPIO.setup(MOTOR,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(ServoPin1, GPIO.OUT)
    GPIO.setup(ServoPin2, GPIO.OUT)
    GPIO.setup(TrackSensorLeftPin1,GPIO.IN)
    GPIO.setup(TrackSensorLeftPin2,GPIO.IN)
    GPIO.setup(TrackSensorRightPin1,GPIO.IN)
    GPIO.setup(TrackSensorRightPin2,GPIO.IN)
    #设置车轮电机pwm引脚和频率为500hz
    pwm_ENA = GPIO.PWM(ENA, 500)
    pwm_ENB = GPIO.PWM(ENB, 500)
    #设置风扇电机pwm引脚和频率为50hz
    pwm_FAN = GPIO.PWM(MOTOR, 50)
    pwm_ENA.start(0)
    pwm_ENB.start(0)
    pwm_FAN.start(100)

#小车前进
def run(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

#小车后退
def back(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)
	
#小车左转	
def left(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

#小车右转
def right(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)
	
#小车原地左转
def spin_left(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

#小车原地右转
def spin_right(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

# 右后方倒车
def back_right(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)
    time.sleep(0.4)


# 左后方倒车
def back_left(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)
    time.sleep(0.4)

#小车停止
def brake():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    
#红灯亮  
def redlight():
    GPIO.output(LED_R, GPIO.HIGH)
    GPIO.output(LED_G, GPIO.LOW)
    GPIO.output(LED_B, GPIO.LOW)
    
#绿灯亮   
def greenlight():
    GPIO.output(LED_R, GPIO.LOW)
    GPIO.output(LED_G, GPIO.HIGH)
    GPIO.output(LED_B, GPIO.LOW)
    
#蓝灯亮
def bluelight():
    GPIO.output(LED_R, GPIO.LOW)
    GPIO.output(LED_G, GPIO.LOW)
    GPIO.output(LED_B, GPIO.HIGH)

#超声波函数
def Distance_test():
    GPIO.output(TrigPin,GPIO.HIGH)
    #高电平至少持续10us以触发超声波模块的测距功能
    time.sleep(0.000015)  
    GPIO.output(TrigPin,GPIO.LOW)
    while not GPIO.input(EchoPin):
        pass
    t1 = time.time()  
    #等待接收引脚高电平结束
    while GPIO.input(EchoPin):
        pass
    t2 = time.time()
    print "distance is %d" % (((t2 - t1)* 340 / 2) * 100)
    time.sleep(0.01)
    return ((t2 - t1)* 340 / 2) * 100

#风扇转动
def fanrun(value):
    pwm_FAN.ChangeDutyCycle(value)

#摄像头舵机转动
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
    for pos in range(60,135):
        servo_pulse2(pos)
        #time.sleep(0.009)

    for pos in reversed(range(60,135)):
        servo_pulse2(pos)
        #time.sleep(0.009)

#摄像头转动
def servo_round():
    while True: 
        servo_control1()
        servo_control2()

#发送邮件    
def send_email(recipient,subject,text):
    smtpserver = smtplib.SMTP(SMTP_SERVER,SMTP_PORT)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(QQMAIL_USER,QQMAIL_PASS)
    header = 'To:'+recipient+'\n'+'From:'+QQMAIL_USER
    header = header + '\n' +'Subject:' + subject +'\n'
    msg = header +'\n'+text+'\n\n'
    smtpserver.sendmail(QQMAIL_USER,recipient,msg)
    smtpserver.close()
    
#蜂鸣器
def sound():
    GPIO.setup(key,GPIO.OUT)
    GPIO.output(key,GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(key,GPIO.HIGH)
    time.sleep(0.5)
    
#巡线返程
def backreturn():
    while True:
        #返程时亮蓝灯
        bluelight()
        
        TrackSensorLeftValue1  = GPIO.input(TrackSensorLeftPin1)
        TrackSensorLeftValue2  = GPIO.input(TrackSensorLeftPin2)
        TrackSensorRightValue1 = GPIO.input(TrackSensorRightPin1)
        TrackSensorRightValue2 = GPIO.input(TrackSensorRightPin2)
        
        if TrackSensorLeftValue1 == False and TrackSensorLeftValue2 == False and TrackSensorRightValue1==False and TrackSensorRightValue2 == False:
            parking()
            break
        if (TrackSensorLeftValue1 == False or TrackSensorLeftValue2 == False) and  TrackSensorRightValue2 == False:
           spin_right(40, 40)
           time.sleep(0.08)
            
        elif TrackSensorLeftValue1 == False and (TrackSensorRightValue1 == False or  TrackSensorRightValue2 == False):
           spin_left(40, 40)
           time.sleep(0.08)
            
        elif TrackSensorLeftValue1 == False:
           spin_left(30, 30)
        
        elif TrackSensorRightValue2 == False:
           spin_right(30, 30)
          
        elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == True:
           left(0,30)
          
        elif TrackSensorLeftValue2 == True and TrackSensorRightValue1 == False:
           right(30, 0)
           
        elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == False:
           run(10, 10)    

#掉头
def round():
    spin_right(80,80)
    time.sleep(0.40)
    
#入库    
def parking():
    brake()
    time.sleep(0.5)

    # 挂倒挡
    back_right(35, 0)
    brake()
    time.sleep(0.5)
    back(30, 30)
    time.sleep(0.6)
    back_left(0, 30)
    # 停车
    brake()
    time.sleep(0.6)

#火源识别
def camera_use():
    lower_green= np.array([50, 100, 100])
    upper_green = np.array([70, 255, 255])
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    global cap 
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('img',frame)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        if cv2.countNonZero(mask_red) > cv2.countNonZero(mask_green) :
            print("find fire")
            return 1
        elif cv2.countNonZero(mask_green) > cv2.countNonZero(mask_red):
            print("green")
        key=cv2.waitKey(1000//24)
        if key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    
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
    
    thread1 = threading.Thread(target=servo_round)
    thread1.setDaemon(True)
    thread1.start()
    
    while True:
        #巡线时亮绿灯
        greenlight()
        
        #检测到黑线时循迹模块相应的指示灯亮，端口电平为LOW
        #未检测到黑线时循迹模块相应的指示灯灭，端口电平为HIGH
        TrackSensorLeftValue1  = GPIO.input(TrackSensorLeftPin1)
        TrackSensorLeftValue2  = GPIO.input(TrackSensorLeftPin2)
        TrackSensorRightValue1 = GPIO.input(TrackSensorRightPin1)
        TrackSensorRightValue2 = GPIO.input(TrackSensorRightPin2)
       
        #处理右锐角和右直角的转动
        if (TrackSensorLeftValue1 == False or TrackSensorLeftValue2 == False) and  TrackSensorRightValue2 == False:
           spin_right(40, 40)
           time.sleep(0.08)
 
        #处理左锐角和左直角的转动
        elif TrackSensorLeftValue1 == False and (TrackSensorRightValue1 == False or  TrackSensorRightValue2 == False):
           spin_left(40, 40)
           time.sleep(0.08)
  
        #最左边检测到
        elif TrackSensorLeftValue1 == False:
           spin_left(30, 30)
           
        #最右边检测到
        elif TrackSensorRightValue2 == False:
           spin_right(30, 30)
          
        #处理左小弯
        elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == True:
           left(0,30)
          
        #处理右小弯
        elif TrackSensorLeftValue2 == True and TrackSensorRightValue1 == False:
           right(30, 0) 

        #处理直线
        elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == False:
           run(10, 10)
                 
        #当为1 1 1 1时小车停止
        else:
            distance = Distance_test()
            if distance > 50:
                pass
            else:
                brake()
                time.sleep(1)
                break
            
    send_email(recipient1,sub1,text1)#发送邮件
    
    myColor=camera_use()
    cap.release()
    cv2.destroyAllWindows()
    
    starttime=time.time()
    nowtime=time.time()
    while nowtime-starttime < 30:
        redlight()
        sound()
        distance = Distance_test()
        if distance > 200:
            fanrun(5)
        elif distance < 10:
            fanrun(100)
        else :
            v=int(1000/distance)
            fanrun(v)
        time.sleep(1)
        nowtime=time.time()
            
    fanrun(100) 
    time.sleep(2)
    
    round()
    brake()
    
    backreturn() #巡线返程
        
       
    
except KeyboardInterrupt:
    pass

#_async_raise(thread1.ident, SystemExit)
pwm_ENA.stop()
pwm_ENB.stop()
pwm_FAN.stop()
GPIO.cleanup()