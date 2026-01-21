

import cv2
import matplotlib.pyplot as plt
import os

# Define the base path and read the image
base_path = os.path.dirname(__file__)
image_path = os.path.join(base_path, r"C:\Users\Student\Documents\megalodon-rov-25-26\Training\thumbs_up_down (1).jpg")

# Read the image
image = cv2.imread(image_path)

# Convert to RGB (for proper display with matplotlib)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# Create a binary thresholded image
_, binary = cv2.threshold(gray, 225, 225, cv2.THRESH_BINARY_INV)

# # Show binary image
# plt.imshow(binary, cmap="gray")
# plt.axis("off")
# plt.show()


# find the contours from the thresholded image
contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# draw all contours
image = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
# show the image with the drawn contours
plt.imshow(image)
plt.show()

