import cv2
import numpy as np
# import os

# base_path = os.path.dirname(__file__)
# sara = cv2.imread(os.path.join(base_path, 'baldrat.jpg'), 1)
sara = cv2.imread(r'C:\\Users\\Student\\megalodon-rov-25-26\\Training\\baldrat.jpg', 1)
cv2.imshow('My Image', sara)
cv2.waitKey(0)
