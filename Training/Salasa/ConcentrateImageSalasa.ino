import cv2

img1 = cv2.imread('baldrat.jpg')
img2 = cv2.imread('baldrat.jpg')
#vertically concentrate images 
con = cv2.vconcat([img1, img2])
cv2.imshow('Concatenated Image', con)
