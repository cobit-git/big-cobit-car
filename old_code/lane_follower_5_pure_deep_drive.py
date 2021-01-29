
import cv2
import logging
import RPi.GPIO as IO
import time 
from adafruit_servokit import ServoKit
from cobit_deep_follower import CobitDeepFollower

pwmPin = 19
dirPin = 13

prev_time  = 0
curr_time = 0

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

cobit_deep_follower = CobitDeepFollower()
cap = cv2.VideoCapture(0)

cap.set(3, int(SCREEN_WIDTH))
cap.set(4, int(SCREEN_HEIGHT))

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(pwmPin, IO.OUT)
IO.setup(dirPin,IO.OUT)

p = IO.PWM(pwmPin, 100)
p.start(0)

# skip first second of video.
for i in range(3):
    _, frame = cap.read()

#video_type = cv2.VideoWriter_fourcc(*'XVID')
#video_overlay = cv2.VideoWriter("%s_deep_drive.avi" % video_file, video_type, 20.0, (320, 240))
p.ChangeDutyCycle(70)

try:
    i = 0
    while cap.isOpened():
        _, frame = cap.read()
        frame_copy = frame.copy()
        logging.info('Frame %s' % i)
        #lane_lines, img_lane = cobit_lane_follower.get_lane(frame)
        #angle_lane, combo_image1 = cobit_lane_follower.get_steering_angle(img_lane, lane_lines)
        prev_time = time.time()
        angle_deep, combo_image2 = cobit_deep_follower.follow_lane(frame_copy)
        curr_time = time.time()
        
        print(angle_deep, curr_time - prev_time)
        kit.servo[0].angle = angle_deep
        #logging.info("desired=%3d, model=%3d, diff=%3d" %
        #                (hand_coded_lane_follower.curr_steering_angle,
        #                end_to_end_lane_follower.curr_steering_angle,
        #                diff))
        #video_overlay.write(combo_image2)
        #cv2.imshow("Lane Detection", combo_image1)
        cv2.imshow("Deep Learning", combo_image2)

        i += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
        IO.output(dirPin, False) 
        IO.output(pwmPin, False)
        IO.cleanup() 
        cap.release()
        video_overlay.release()
        cv2.destroyAllWindows()


        
