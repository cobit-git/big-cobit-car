import cv2
import logging
from cobit_lane_follower import CobitLaneFollower
from cobit_deep_follower import CobitDeepFollower
import time

video_file = "data/car_video.avi"

cobit_deep_follower = CobitDeepFollower()
cobit_lane_follower = CobitLaneFollower()
cap = cv2.VideoCapture(video_file)

prev_time = 0
curr_time  = 0

# skip first second of video.
for i in range(3):
    _, frame = cap.read()

#video_type = cv2.VideoWriter_fourcc(*'XVID')
#video_overlay = cv2.VideoWriter("%s_deep_drive.avi" % video_file, video_type, 20.0, (320, 240))
try:
    i = 0
    while cap.isOpened():
        _, frame = cap.read()
        frame_copy = frame.copy()
        logging.info('Frame %s' % i)
        lane_lines, img_lane = cobit_lane_follower.get_lane(frame)
        angle_lane, combo_image1 = cobit_lane_follower.get_steering_angle(img_lane, lane_lines)
        
        prev_time = time.time()
        angle_deep, combo_image2 = cobit_deep_follower.follow_lane(frame_copy)
        curr_time = time.time()

        diff = angle_lane - angle_deep
        print(angle_deep, angle_lane, curr_time-prev_time)
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
    cap.release()
    video_overlay.release()
    cv2.destroyAllWindows()
