import cv2
import os
import undistortCameras
import glob
import numpy as np

CALIB_FILE = os.path.join(os.path.dirname(__file__), "calib_data.npz")

if not os.path.exists(CALIB_FILE):
    print("Calibration file not found. Please run calibrateCameras.py first.")
else:
    data = np.load(CALIB_FILE)
    mtx = data['mtx']
    dist = data['dist']
    w = data['w']
    h = data['h']

newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (frame_width, frame_height), 0, (frame_width, frame_height))
mapx, mapy=cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (frame_width, frame_height), 5)

def take_video():
    base_path = os.path.dirname(__file__)

    # Open the robot's camera
    cam1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam2 = cv2.VideoCapture(0, cv2.CAP_DSHOW)       # use cv2.CAP_DSHOW to tell openCV
                                                    # to use camera driver backend
                                                    # instead of default backend

    # Get the default frame width and height
    frame_width1 = int(cam1.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height1 = int(cam1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_width2 = int(cam2.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height2 = int(cam2.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object. 
    # For the VideoWriter func, may have to switch path.
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # find new file to write still-distorted video into
    index = 0
    videoPath1 = os.path.join(base_path, "measuring_vid" + str(index) + ".mp4")
    videoPath2 = os.path.join(base_path, "measuring_vid" + str(index) + ".mp4")
    while os.path.exists(videoPath1):
        index += 1
        videoPath1 = os.path.join(base_path, "measuring_vid" + str(index) + ".mp4")
    index += 1
    videoPath2 = os.path.join(base_path, "measuring_vid" + str(index) + ".mp4")
    out1 = cv2.VideoWriter(videoPath1, fourcc, 20.0, (frame_width1, frame_height1))
    out2 = cv2.VideoWriter(videoPath2, fourcc, 20.0, (frame_width2, frame_height2))

    print("Recording video. Press 'q' to stop recording.")

    while True:
        ret1, frame1 = cam1.read()
        ret2, frame2 = cam2.read()

        if ret1:
            # Write the frame to the output file3
            out1.write(cv2.remap(frame1, mapx, mapy, cv2.INTER_LINEAR))

            # Display the captured frame
            cv2.imshow('Camera 1', frame1)

            # Press 'q' to exit the loop
            if cv2.waitKey(1) == ord('q'):
                break
        
        else:
            print("Failed to capture frame from camera 1")

        if ret2:
            # Write the frame to the output file
            out2.write(cv2.remap(frame2, mapx, mapy, cv2.INTER_LINEAR))

            # Display the captured frame
            cv2.imshow('Camera 2', frame2)

            # Press 'q' to exit the loop
            if cv2.waitKey(1) == ord('q'):
                break
        
        else:
            print("Failed to capture frame from camera 2")

    # Release the capture and writer objects
    cam1.release()
    cam2.release()
    out1.release()
    out2.release()
    cv2.destroyAllWindows()

    undistortedVideoPath = os.path.join(base_path, "measuring_vid_undistorted" + str(index) + ".mp4")

    undistortCameras.undistort(videoPath, undistortedVideoPath)
    return undistortedVideoPath        # return the path to the video file for later use in image processing

if __name__ == "__main__":
    take_video()