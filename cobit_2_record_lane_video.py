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

# Below code works normally for Pi camera V2.1
# But for ELP webcam, it doesn't work.
#fourcc =  cv2.VideoWriter_fourcc(*'XVID')
fourcc =  cv2.VideoWriter_fourcc('M','J','P','G')

video_orig = cv2.VideoWriter('./data/car_video.avi', fourcc, 20.0, (SCREEN_WIDTH, SCREEN_HEIGHT))
#video_lane = cv2.VideoWriter('./data/car_video_lane.avi', fourcc, 20.0, (SCREEN_WIDTH, SCREEN_HEIGHT))


servo_offset = 15
      
for i in range(3):
	_, frame = cap.read()
     
motor.motor_all_start(20)

while True:
	ret, img_org = cap.read()
	if ret:
		
		video_orig.write(img_org)
		
		lanes, img_lane = cv_detector.get_lane(img_org)
		angle, img_angle = cv_detector.get_steering_angle(img_lane, lanes)
		if img_angle is None:
			print("angle image out!!")
			pass
		else:
			#video_lane.write(img_lane)
			
			print(angle)
			servo.servo[0].angle = angle+ servo_offset
		cv2.imshow('img_org', img_org)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	else:
		print("cap error")
		
motor.motor_all_stop()
cap.release()
video_orig.release()
#video_lane.release()
cv2.destroyAllWindows()
