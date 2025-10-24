import cv2
import numpy as np

#connect to deafult camera
camera = cv2.VideoCapture(0)
#find width and height of live feed
width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
