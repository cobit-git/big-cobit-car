import cv2
from adafruit_servokit import ServoKit
from cobit_opencv_lane_detect import CobitOpencvLaneDetect
from cobit_car_motor_l9110 import CobitCarMotorL9110

cv_detector = CobitOpencvLaneDetect()
motor = CobitCarMotorL9110()
servo = ServoKit(channels=16)

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240

cap = cv2.VideoCapture(0)
cap.set(3, int(SCREEN_WIDTH))
cap.set(4, int(SCREEN_HEIGHT))

servo_offset = 15

motor.motor_all_start(30)

while True:
	ret, img_org = cap.read()
	
	if ret:
		lanes, img_lane = cv_detector.get_lane(img_org)
		angle, img_angle = cv_detector.get_steering_angle(img_lane, lanes)
		if img_angle is None:
			print("angle image out!!")
			pass
		else:
			print(angle)
			servo.servo[0].angle = angle + servo_offset
		cv2.imshow("img_org", img_org)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	else:
		print("cap error")

cap.release()
cv2.destroyAllWindows()
