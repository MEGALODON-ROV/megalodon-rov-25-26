import cv2
import os

base_path = os.path.dirname(__file__)
img1 = cv2.imread(os.path.join(base_path, 'baldrat.jpg'), 1)
img2 = cv2.imread(os.path.join(base_path, 'baldrat.jpg'), 1)

# img1 = cv2.imread('baldrat.jpg')
# img2 = cv2.imread('baldrat.jpg')
if img1.shape != img2.shape:
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))


v_con = cv2.vconcat([img1, img2])

cv2.imshow('Concatenated Image', v_con)
cv2.waitKey(0)
cv2.destroyAllWindows()
