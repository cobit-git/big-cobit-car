import cv2
from adafruit_servokit import ServoKit
from cobit_deep_lane_detect import CobitDeepLaneDetect
from cobit_car_motor_l9110 import CobitCarMotorL9110

servo = ServoKit(channels=16)
deep_detector = CobitDeepLaneDetect("./models/lane_navigation_final.h5")
motor = CobitCarMotorL9110()
cap = cv2.VideoCapture(0)

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240

cap.set(3, SCREEN_WIDTH)
cap.set(4, SCREEN_HEIGHT)

# skip first second of video.
for i in range(3):
    _, frame = cap.read()

motor.motor_all_start(17)

try:
    while cap.isOpened():
        ret, img_org = cap.read()
        angle_deep, img_angle = deep_detector.follow_lane(img_org)
        
        print(angle_deep)
        servo.servo[0].angle = angle_deep
        cv2.imshow("Deep Learning", img_angle)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally: 
        cap.release()
        motor.motor_all_stop()
        cv2.destroyAllWindows()


        
