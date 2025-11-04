import numpy
#import argparse
import cv2
import matplotlib.pyplot as plt
import imutils

#Parser = argparse.ArgumentParser()
#Parser.add_argument("-i", "--image", type=str, default="/Users/matthewhoffmeister/Desktop/KahootImage.jpeg",
	#help="path to the input image")

image = cv2.imread('/Users/matthewhoffmeister/Desktop/KahootImage.jpeg', 1)
reference = image
image2 = image #cv2.imread('/Users/matthewhoffmeister/Desktop/Harris.jpeg', 1)
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
cv2.destroyAllWindows()

image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
imageGrey = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

_, binaryGrey = cv2.threshold(imageGrey, 180, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('test', binaryGrey)

contours, hierarchy = cv2.findContours(binaryGrey, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#cnts = imutils.grab_contours(contours)
#c = max(cnts, key=cv2.contourArea)
image2 = cv2.drawContours(image2, contours, -1, (150, 0, 150), 4)

#cv2.imshow('contoured', image2)
plt.imshow(image2, cmap='gray')
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()

class detector:
    def __init__(self):
        pass

    def detect(self, c):
        shape = "unknown"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        if len(approx) == 3:
            shape = "triangle"

        elif len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)

            if ar > 0.95 and ar < 1.05:
                shape = "square"
            else:
                shape = "rectangle"

        if len(approx) == 5:
            shape = "pentagon"

        if len(approx) == 6:
            shape = "hexagon"
        
        else:
            shape = "circle"

        return shape

    for i in contours:
        M = cv2.moments(i)
        cX = int((M["m10"] / M["m00"]))
        cY = int((M["m01"] / M["m00"]))
        shape = detect(i, i)

        cv2.drawContours(image2, [i], -1, (0, 255, 0), 2)
        cv2.putText(image2, shape, (cX, cY - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 5)
        
    cv2.imshow("shapes", image2)

cv2.waitKey(0)
cv2.destroyAllWindows()

refPt = []
cropping = False

def clickCrop(event, x, y, flags, param):
    global refPt, cropping

    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False
        newIm = image.copy()
        cv2.rectangle(newIm, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("image", newIm)

    elif event == cv2.EVENT_MOUSEMOVE and cropping:
        newIm = image.copy()
        cv2.rectangle(newIm, refPt[0], (x, y), (0, 255, 0), 2)
        cv2.destroyWindow("drawing")
        cv2.imshow("drawing", newIm)

cv2.namedWindow("image")
cv2.setMouseCallback("image", clickCrop)

while True:
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("r"):
        image = reference.copy()
        newIm = reference.copy()
        cv2.destroyWindow("drawing")
        refPt = []

    elif key == ord("c"):
        break

if len(refPt) == 2:
    roi = image[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    cv2.imshow("ROI", roi)
    cv2.waitKey(0)

cv2.waitKey(0)
cv2.destroyAllWindows()

camera = cv2.VideoCapture(0)

width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output = cv2.VideoWriter('/Users/matthewhoffmeister/Desktop/finalCamera.mp4', fourcc, 30, (width, height))

while True:
    ret, frame = camera.read()

    output.write(frame)
    cv2.imshow("finalCamera", frame)

    if cv2.waitKey(1) == ord('c'):
        image = frame
        cv2.destroyAllWindows()
        break

camera.release()
output.release()

refPt = []
cv2.namedWindow("image")
cv2.setMouseCallback("image", clickCrop)

while True:
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("r"):
        newIm = reference.copy()
        cv2.destroyWindow("drawing")
        refPt = []

    elif key == ord("c"):
        break

if len(refPt) == 2:
    roi = image[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    cv2.imshow("ROI", roi)
    cv2.waitKey(0)


cv2.waitKey(0)