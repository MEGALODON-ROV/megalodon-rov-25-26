import cv2
import calibrateCameras as calib
import video_taking as vid

FRONTCAM = 1
BOTTOMCAM = 2

def findCamIndex(camSide = "FRONT"):
    for i in range(10):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():      # camera exists at the index
            print("Is this {} camera? (Y/N): ".format(camSide))
            while True:
                ret, frame = cap.read()

                if ret:
                    # Display the captured frame
                    cv2.imshow('Camera', frame)

                    # Press 'q' to exit the loop
                    if cv2.waitKey(1) == ord('y') or cv2.waitKey(1) == ord('Y'):
                        cap.release()
                        cv2.destroyAllWindows()
                        return i
                    elif cv2.waitKey(1) == ord('n') or cv2.waitKey(1) == ord('N'):
                        cap.release()
                        cv2.destroyAllWindows()
                        break

    return 0

def main():
    windows = True

    usesWindows = input("Do you use a windows computer? (Y/N): ")   # might not implement
    if (usesWindows.lower() == 'n'):
        windows = False
        print("Bruh. Lock in :(")

    print("Please plug in EVERYTHING RIGHT NOW!")       # TODO: perhaps move to oneFrickinFantasticFile since this is general setup?
    plugged = input("Have you plugged in EVERYTHING? (Y/N): ")
    if (plugged.lower() == 'y'):
        FRONTCAM = findCamIndex("FRONT")
        BOTTOMCAM = findCamIndex("BOTTOM")

    shouldCalib = input("Do you want to re-calibrate the camera? (Y/N): ")
    shouldCalib = input("Are you ABSOLUTELY sure? (Y/N): ")
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

if __name__ == "__main__":
    main()