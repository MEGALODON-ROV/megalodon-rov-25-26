import threading
import time
import nav_main
import sys
import os
import cv2

# path to other folders (not Nav) so we can import their files
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'IP')))
import measuringTaskMain as measure
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'image_rec_task')))
import CRAB_TEST

FRONTCAM = 1
BOTTOMCAM = 2

def findCamIndex(camSide = "FRONT"):
    for i in range(10):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():      # camera exists at the index
            print("Is this {} camera? (Y/N): ".format(camSide))
            while True:     # display camera feed
                ret, frame = cap.read()

                if ret:
                    # Display the captured frame
                    cv2.imshow('Camera', frame)

                    # verify if it's the right camera
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('y') or key == ord('Y'):
                        cap.release()
                        cv2.destroyAllWindows()
                        return i
                    elif key == ord('n') or key == ord('N'):
                        cap.release()
                        cv2.destroyAllWindows()
                        break

    return 0

print("Please plug in EVERYTHING RIGHT NOW!")
plugged = input("Have you plugged in EVERYTHING? (Y/N): ")
if (plugged.lower() == 'y'):
    FRONTCAM = findCamIndex("FRONT")
    BOTTOMCAM = findCamIndex("BOTTOM")

navigation = threading.Thread(target=nav_main.nav, daemon=False)
navigation.start()

while True:
    program = input("What program do you want to run? (1: photogrammetry, 2: image rec, 3: show depth, 4: hide depth, E: exit): ")
    if program == "1":
        measure.main(FRONTCAM)
    elif program == "2":
        #print("Image recognition not implemented yet :(")
        CRAB_TEST.imageRec(BOTTOMCAM)
    elif program == "3":
        nav_main.displayDepth = True
    elif program == "4":
        nav_main.displayDepth = False
    elif program.lower() == "e":
        print("Exiting...")
        nav_main.loop = False
        break
    else:
        print("Invalid input. Please enter 1, 2, 3, 4, or E.")

    time.sleep(1)