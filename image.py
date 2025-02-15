#-*- coding:UTF-8 -*-
import cv2
import RPi.GPIO as GPIO
import time
servo_pin = 11
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)
def rotate_camera(angle):
    duty = angle / 18 + 2
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)
cap = cv2.VideoCapture(0)
while True:
    # 读取摄像头图像
    frame = cap.read()
    # 显示图像
    cv2.imshow("Camera", frame)
    # 按q键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # 按a键摄像头向左转
    if cv2.waitKey(1) & 0xFF == ord('a'):
        rotate_camera(0)
    # 按d键摄像头向右转
    if cv2.waitKey(1) & 0xFF == ord('d'):
        rotate_camera(180)
cap.release()
cv2.destroyAllWindows()
pwm.stop()
GPIO.cleanup()