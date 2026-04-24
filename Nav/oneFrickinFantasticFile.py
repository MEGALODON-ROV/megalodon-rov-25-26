import threading
import time
#import nav_main
import sys
import os

# path to other folders (not Nav) so we can import their files
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'IP')))
import measuringTaskMain as measure
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'image_rec_task')))
import CRAB_TEST


FRONTCAM = 1
BOTTOMCAM = 2
print("Please plug in EVERYTHING RIGHT NOW!")
plugged = input("Have you plugged in EVERYTHING? (Y/N): ")
if (plugged.lower() == 'y'):
    FRONTCAM = measure.measuringTaskMain.findCamIndex("FRONT")
    BOTTOMCAM = measure.measuringTaskMain.findCamIndex("BOTTOM")

#navigation = threading.Thread(target=nav_main.nav, daemon=True)
#navigation.start()

while True:
    program = input("What program do you want to run? (1: photogrammetry, 2: image rec, E: exit): ")
    if program == "1":
        measure.main(FRONTCAM, BOTTOMCAM)
    elif program == "2":
        CRAB_TEST.imageRec()
    elif program.lower() == "e":
        print("Exiting...")
        break
    else:
        print("Invalid input. Please enter 1, 2, or E.")

    time.sleep(1)