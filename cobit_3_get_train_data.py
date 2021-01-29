import cv2
import sys
from cobit_opencv_lane_detect import CobitOpencvLaneDetect

video_file = sys.argv[1]
cv_detector = CobitOpencvLaneDetect()

cap = cv2.VideoCapture(video_file)
i = 0

while True:
	ret, img_org = cap.read()
	if ret:
		lanes, img_lane = cv_detector.get_lane(img_org)
		cv2.imshow("ddd", img_org)
		angle, img_angle = cv_detector.get_steering_angle(img_lane, lanes)
		if img_angle is None:
			pass
		else:
			cv2.imwrite("%s_%03d_%03d.png" % (video_file, i, angle), img_org)
			i += 1	
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	else:
		print("cap error")

cap.release()
cv2.destroyAllWindows()
