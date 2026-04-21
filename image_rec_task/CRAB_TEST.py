import os
os.environ["QT_QPA_PLATFORM"] = "xcb" # Forces the standard Linux display bc i kept getting weird errors

import supervision as sv
import cv2
from ultralytics import YOLO
import time


model = YOLO("/home/salasaooo/image_rec/CRAB_6FIN.pt") #copy path of best.pt 

# results = model(source=0, show=True, classes=[0]) #trying to only look for EGC in live feed 

print(f" looking for: {model.names}") #double check what its looking for 


#  Setup Camera
cam = cv2.VideoCapture(0)


if not cam.isOpened():
    print(": Could not open camera")
    exit()
else:
    print("Camera found!  ...")
    cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    time.sleep(2)
# time.sleep(2)
# frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
# frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fps =cam.get(cv2.CAP_PROP_FPS)

# Video Recording Setup
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('crab_mission.mp4', fourcc, 20.0, (640, 480))

print("Starting  Video. Press 'q' to stop.")

while True:
    ret, frame = cam.read()
    if not ret:
        break
    results = model(frame, conf=0.5, iou=0.5, classes=[0])
    result = results[0] #only egc 


    if len(result.boxes) > 0:
        print(f"Detected {len(result.boxes)} objects!")
    else:
        print("... scanning ...")

    annotated_frame = result.plot()

    text = f'European Green Crabs: {len(result.boxes)}'
    position = (10, 30)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (0, 255, 0)  # Green color
    thickness = 2
    cv2.putText(annotated_frame, text, position, font, font_scale, color, thickness)
    out.write(annotated_frame)

    cv2.imshow('LIVE FEED', annotated_frame)

    if cv2.waitKey(1) == ord('q'):
        break



# 
cam.release()
out.release()
cv2.destroyAllWindows()

print(f"done done")
