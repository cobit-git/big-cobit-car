import imutils
import RPi.GPIO as IO
import cv2
import datetime
from adafruit_servokit import ServoKit
from cobit_lane_follower import CobitLaneFollower

pwmPin = 19
dirPin = 13

#pwmPin2 = 12
#dirPin2 = 16

#__SCREEN_WIDTH = int(1280/4)
#__SCREEN_HEIGHT = int(720/4)
__SCREEN_WIDTH = 320
__SCREEN_HEIGHT = 240



kit = ServoKit(channels=16)

#SCREEN_WIDTH = int(1280/4) #320
#SCREEN_HEIGHT = int(720/4) #240
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240


lane_follower = CobitLaneFollower()
cap = cv2.VideoCapture(0)

cap.set(3, SCREEN_WIDTH)
cap.set(4, SCREEN_HEIGHT)

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


#p2.ChangeDutyCycle(30)

# Below code works normally for Pi camera V2.1
# But for ELP webcam, it doesn't work.
#fourcc =  cv2.VideoWriter_fourcc(*'XVID')
fourcc =  cv2.VideoWriter_fourcc('M','J','P','G')

datestr = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
#print(datestr)
#video_orig = create_video_recorder('/data/car_video%s.avi' % datestr)
video_orig = cv2.VideoWriter('./data/car_video.avi', fourcc, 20.0, (__SCREEN_WIDTH, __SCREEN_HEIGHT))
#video_lane = create_video_recorder('/data/car_video_lane%s.avi' % datestr)
video_lane = cv2.VideoWriter('./data/car_video_lane.avi', fourcc, 20.0, (__SCREEN_WIDTH, __SCREEN_HEIGHT))
      
# skip first second of video.
for i in range(3):
	_, frame = cap.read()
p.ChangeDutyCycle(30)      

while True:
	ret, img_org = cap.read()
	if ret:
		cv2.imshow('lane', img_org)
		video_orig.write(img_org)
		lane_lines, img_lane = lane_follower.get_lane(img_org)
		
		angle, img_lane = lane_follower.get_steering_angle(img_lane, lane_lines)
		if img_lane is None:
			pass
		else:
			video_lane.write(img_lane)
			
			print(angle)
			kit.servo[0].angle = angle
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	else:
		print("cap error")
p.ChangeDutyCycle(0)
cap.release()
video_orig.release()
video_lane.release()
cv2.destroyAllWindows()
