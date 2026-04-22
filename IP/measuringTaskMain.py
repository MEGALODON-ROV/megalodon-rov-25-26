import cv2
import calibrateCameras as calib
import video_taking as vid
from cv2_enumerate_cameras import enumerate_cameras

FRONTCAM = 1

def findCamIndex():
    for i in range(10):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():      # camera exists at the index
            print("Is this FRONT camera? (Y/N): ")
            while True:
                ret, frame = cap.read()

                if ret:
                    # Display the captured frame
                    cv2.imshow('Camera', frame)

                    # Press 'q' to exit the loop
                    if cv2.waitKey(1) == ord('y') or cv2.waitKey(1) == ord('Y'):
                        cap.release()
                        return i
                    elif cv2.waitKey(1) == ord('n') or cv2.waitKey(1) == ord('N'):
                        cap.release()
                        break

    return 0

windows = True

usesWindows = input("Do you use a windows computer? (Y/N): ")
if (usesWindows.lower() == 'n'):
    windows = False
    print("Bruh. Lock in :(")

print("Please plug in EVERYTHING RIGHT NOW!")
plugged = input("Have you plugged in EVERYTHING? (Y/N): ")
if (plugged.lower() == 'y'):
    FRONTCAM = findCamIndex()

shouldCalib = input("Do you want to re-calibrate the camera? (Y/N): ")
if (shouldCalib.lower() == 'y'):
    print("Instructions:")
    print("1. Place 8x5 inner corner (colxrow) checkerboard in front of the camera.")
    print("2. Take pictures of the checkerboard from multiple angles and distances.")
    print("3. Full checkerboard must be in view of camera.")
    print("Hint: take > 40 pictures to be very safe!")
    print("Press 's' to save an image, and 'q' to quit the camera feed.")
    calib.calibrate_camera(FRONTCAM)

shouldTakeVid = input("Do you want to take a video for measuring now? (Y/N): ")
if (shouldTakeVid.lower() == 'n'):
    print("Womp. Run me when you're ready next time :(")
else:
    print("Hint: Please move slowly while taking the video to avoid blurring!")
    videoPath = vid.take_video(FRONTCAM)
    print("Path to undistorted video: {}".format(videoPath))