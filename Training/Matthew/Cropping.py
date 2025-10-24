import numpy
#import argparse
import cv2
#import imutils

#Parser = argparse.ArgumentParser()
#Parser.add_argument("-i", "--image", type=str, default="/Users/matthewhoffmeister/Desktop/KahootImage.jpeg",
	#help="path to the input image")

image = cv2.imread('/Users/matthewhoffmeister/Desktop/KahootImage.jpeg', 1)
print(image.shape[0])
cv2.imshow('Original',image)

cv2.waitKey(0)
cv2.destroyAllWindows()


r = 748/512
Dim = (150, round(150 / r))
resized = cv2.resize(image, Dim, cv2.INTER_AREA)
cv2.imshow('New', resized)

cv2.waitKey(0)
cv2.destroyAllWindows()

cch = resized
timer = 1

while timer < 4:
    newDim = (150 * pow(2, timer), round((150 * pow(2, timer)) / r))
    newIm = cv2.resize(resized, newDim, cv2.INTER_AREA)
    cch = cv2.hconcat([cch, cch])
    cch = cv2.vconcat([newIm, cch])
    timer += 1

cv2.imshow('Horizontal',cch)

cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow('original',image)
cv2.putText(image, "+1000", (200,300), cv2.FONT_HERSHEY_SIMPLEX, 5, (255,255,255), 10, cv2.LINE_AA)
cv2.imshow('drawing', image)

cv2.waitKey(0)

#748 * 512