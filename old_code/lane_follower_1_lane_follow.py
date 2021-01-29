import imutils
import RPi.GPIO as IO
import cv2
import datetime
import time 
from adafruit_servokit import ServoKit
from cobit_lane_follower import CobitLaneFollower

pwmPin = 19
dirPin = 13

#pwmPin2 = 12
#dirPin2 = 16

__SCREEN_WIDTH = 1280/4
__SCREEN_HEIGHT = 720/4
#__SCREEN_WIDTH = 320
#__SCREEN_HEIGHT = 240

kit = ServoKit(channels=16)

SCREEN_WIDTH = 1280/4
SCREEN_HEIGHT =720/4
#SCREEN_WIDTH = 320
#SCREEN_HEIGHT = 240


lane_follower = CobitLaneFollower()
cap = cv2.VideoCapture(0)

cap.set(3, int(SCREEN_WIDTH))
cap.set(4, int(SCREEN_HEIGHT))

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(pwmPin, IO.OUT)
IO.setup(dirPin,IO.OUT)
#IO.setup(pwmPin2, IO.OUT)
#IO.setup(dirPin2,IO.OUT)

p = IO.PWM(pwmPin, 100)
p.start(0)

#p2 = IO.PWM(pwmPin2, 100)
#p2.start(0)

p.ChangeDutyCycle(50)
#p2.ChangeDutyCycle(20)

while True:
	ret, img_org = cap.read()
	if ret:
		lane_lines, img_lane = lane_follower.get_lane(img_org)
		angle, img_lane = lane_follower.get_steering_angle(img_lane, lane_lines)
		if img_lane is None:
			pass
		else:
			print(angle)
			kit.servo[0].angle = angle
			cv2.imshow("img_org", img_org)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	else:
		print("cap error")

cap.release()
cv2.destroyAllWindows()
