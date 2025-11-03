import numpy as np
import os
import imutils
import cv2

base_path = os.path.dirname(__file__)
image_path = r"C:\Users\Yusuke\megalodon-rov-25-26\Training\output.webp"  # Use direct path
print(f"Loading image from: {image_path}")
# load the image and display it
image = cv2.imread(image_path)
cv2.imshow("Image", image)
# convert the image to grayscale and threshold it
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]  # use normal binary threshold
cv2.imshow("Thresh", thresh)


# # Wait for a key press and then close all windows
cv2.waitKey(0)


# find the largest contour in the threshold image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
c = max(cnts, key=cv2.contourArea)
# draw the shape of the contour on the output image, compute the
# bounding box, and display the number of points in the contour
output = image.copy()
cv2.drawContours(output, [c], -1, (0, 255, 0), 3)
(x, y, w, h) = cv2.boundingRect(c)
text = "original, num_pts={}".format(len(c))
cv2.putText(output, text, (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX,
	0.9, (0, 255, 0), 2)
# show the original contour image
print("[INFO] {}".format(text))
cv2.imshow("Original Contour", output)
cv2.waitKey(0)

# to demonstrate the impact of contour approximation,'s loop
# over a number of epsilon sizes
for eps in np.linspace(0.001, 0.05, 10):
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, eps * peri, True)
	# draw the approximated contour on the image
	output = image.copy()
	cv2.drawContours(output, [approx], -1, (0, 255, 0), 3)
	text = "eps={:.4f}, num_pts={}".format(eps, len(approx))
	cv2.putText(output, text, (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX,
		0.9, (0, 255, 0), 2)
	# show the approximated contour image
	print("[INFO] {}".format(text))
	cv2.imshow("Approximated Contour", output)
cv2.waitKey(0)
cv2.destroyAllWindows()

