import cv2
import numpy as np
import os

base_path = os.path.dirname(__file__)

# GET A VIDEO AND SNAPSHOT
camera = cv2.VideoCapture(0)    # 0 is usually the built-in webcam

# dimentions of the camera feed
width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

# codec = device/program that compresses data for faster transmission and
# decompresses data for receiving
# define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # four character code saying how to encode/decode video
outputFile = cv2.VideoWriter(os.path.join(base_path, "finalProjCam.mp4"), fourcc, 20.0, (width, height)) # 20.0 is fps, output.mp4
                                                                          # is name of saved video file
savedFile = ""
while True:
    captured, frame = camera.read()   # read() returns 2 values, first is boolean
                                      # saying if frame was captured successfully

    # write frame to the output file
    if captured:
        outputFile.write(frame)
        cv2.imshow("Camera Feed", frame)   # display the frame in a window
                                            # for continuous video footage

    # press "q" to exit loop
    if cv2.waitKey(1) == ord("q"):
        break
    if cv2.waitKey(1) == ord("s"):
        beginNum = 0
        while os.path.exists(os.path.join(base_path, "finalProjSnapshot"+str(beginNum)+".jpg")):
            beginNum += 1
        savedFile = os.path.join(base_path, "finalProjSnapshot"+str(beginNum)+".jpg")
        cv2.imwrite(savedFile, frame)
        print("Image saved!")
        break

# release the capture and writer objects and close any open windows
camera.release()
outputFile.release()
cv2.destroyAllWindows()

file = cv2.imread(savedFile, cv2.IMREAD_COLOR)
points = []

def click_event(event, x, y, flags, params):        # flags and params given by OpenCV
    global points, file

    if event == cv2.EVENT_LBUTTONDOWN:     # left mouse button clicked
        points.append((x, y))
        cv2.circle(file, points[-1], 5, (0, 0, 255), -1)   # draw most recent point

cv2.imshow("Snapshot", file)
cv2.setMouseCallback("Snapshot", click_event)

while True:
    cv2.imshow("Snapshot", file)
    key = cv2.waitKey(1)

    if len(points) == 4:
        break

cv2.rectangle(file, points[0], points[2], (0, 255, 0), 2)   # draw rectangle using top-left and bottom-right points
cv2.imshow("Snapshot", file)

cv2.waitKey(0)
cv2.destroyAllWindows()