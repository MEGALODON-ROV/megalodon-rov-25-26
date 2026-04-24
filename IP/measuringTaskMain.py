import cv2
import calibrateCameras as calib
import video_taking as vid

def main(FRONTCAM = 1):
    windows = True

    usesWindows = input("Do you use a windows computer? (Y/N): ")   # might not implement
    if (usesWindows.lower() == 'n'):
        windows = False

    shouldCalib = input("Do you want to re-calibrate the camera? (Y/N): ")
    if (shouldCalib.lower() == 'y'):
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