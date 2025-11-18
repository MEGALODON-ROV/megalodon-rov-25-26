import cv2
import numpy as np
import os
import imutils

base_path = os.path.dirname(__file__)
sara = cv2.imread(os.path.join(base_path, 'baldrat.jpg'), 1)
# sara = cv2.imread(r'C:\\Users\Student\\megalodon-rov-25-26\\Training\\baldrat.jpg', 1)

cv2.imshow('My Image of Sara', sara)

face = sara[90:450, 0:290] # Crop the image to get the face
cv2.imshow('Cropped Bald Rat', face)

number = 1000
r = 1000.0 / sara.shape[1]
dim = (1000, int(sara.shape[0] * r))
resized = cv2.resize(sara, dim, interpolation=cv2.INTER_AREA)
cv2.imshow(f"Resized by {number}x", resized)
cv2.waitKey(0)

