#-*- coding:utf-8 -*-
import cv2 
import sys
import glob
import serial
import threading
#from threading import Thread 
import time
from adafruit_servokit import ServoKit
from cobit_car_motor_l9110 import CobitCarMotorL9110
from cobit_serial_vehicle_manager import SerialVehicleManager
#from cobit_opencv_cam_rc import CobitOpenCVCamRC

motor = CobitCarMotorL9110()
servo = ServoKit(channels=16)
vehicle = SerialVehicleManager("/dev/ttyUSB0")
#cam = CobitOpenCVCamRC()

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240

cap = cv2.VideoCapture(0)
cap.set(3, int(SCREEN_WIDTH))
cap.set(4, int(SCREEN_HEIGHT))

fourcc =  cv2.VideoWriter_fourcc('M','J','P','G')
video_orig = cv2.VideoWriter('./data/car_video.avi', fourcc, 20.0, (SCREEN_WIDTH, SCREEN_HEIGHT))


vehicle.start()

vehicle.open_port()

#t = threading.Thread(target=vehicle.update, args=())
#t.daemon = True
#t.start

i = 0
video_file = "data/cobit"
angle = 30

while True:
    ret, img_org = cap.read()
    #video_orig.write(img_org)
    cv2.imwrite("%s_%03d_%03d.png" % (video_file, i, angle), img_org)
    i += 1
    if ret:
        cv2.imshow('win', img_org)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("cap error")
cap.release()
cv2.destroyAllWindows()

   





   







