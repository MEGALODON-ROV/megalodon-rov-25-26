import cv2

# detect color of crab rgb(60, 65, 35) - rgb(105, 115, 65)

import cv2
import numpy as np

# --- SETTINGS ---
# Define your target RGB color range (example values)
lower_rgb = np.array([90, 40, 30])   # lower bound of crab color (in RGB)
upper_rgb = np.array([180, 120, 90]) # upper bound of crab color (in RGB)

# --- LOAD IMAGE ---
egc = cv2.imread(r"C:\Users\dogei\Downloads\egc.jpg")
rc = cv2.imread(r"C:\Users\dogei\Downloads\rc.png")

# Convert from BGR (OpenCV default) to RGB
egc_rgb = cv2.cvtColor(egc, cv2.COLOR_BGR2RGB)
rc_rgb = cv2.cvtColor(rc, cv2.COLOR_BGR2RGB)

# --- CREATE MASK ---
# Identify pixels within the color range
"""
- Basically, creates a huge array with each of the pixels in the image
- Each element in the array (each pixel in the img) will either be 255 or 0 depending if it matches the rgb range
"""
egc_mask = cv2.inRange(egc, lower_rgb, upper_rgb)
rc_mask = cv2.inRange(rc, lower_rgb, upper_rgb)


# --- DETECTION LOGIC ---
# If any pixel is within range, print detection message.

pixel_count = np.sum(rc_mask > 0)
if pixel_count > 1000:  # <-- adjust this threshold based on your image size
    print("✅ Target crab color detected!")
else:
    print("❌ Target crab color NOT found.")


"""
print("EGC IMG =")
if np.any(egc_mask > 0):
    print("✅ Target crab color detected!")
else:
    print("❌ Target crab color NOT found.")
print()
print("RC IMG =")
if np.any(rc_mask > 0):
    print("✅ Target crab color detected!")
else:
    print("❌ Target crab color NOT found.")
"""