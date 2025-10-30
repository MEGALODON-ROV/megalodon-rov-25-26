import numpy as np
import argparse
import imutils
import cv2

# load the image and display it
image = cv2.imread("image")
cv2.imshow("Image", image)
# convert the image to grayscale and threshold it
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 200, 255,
	cv2.THRESH_BINARY_INV)[1]
cv2.imshow("Thresh", thresh)