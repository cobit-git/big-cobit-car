
import cv2
import numpy as np

grey = np.uint8([[[40,33,34]]])
hsv_grey = cv2.cvtColor(grey,cv2.COLOR_BGR2HSV)
print(hsv_grey)
