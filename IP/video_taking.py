import cv2
import os

import undistortCameras

def take_video():
    base_path = os.path.dirname(__file__)

    # Open the robot's camera
    cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)        # use cv2.CAP_DSHOW to tell openCV
                                                    # to use camera driver backend
                                                    # instead of default backend

    # Get the default frame width and height
    frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object. 
    # For the VideoWriter func, may have to switch path.
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # find new file to write still-distorted video into
    index = 0
    videoPath = os.path.join(base_path, "measuring_vid" + str(index) + ".mp4")
    while os.path.exists(videoPath):
        index += 1
        videoPath = os.path.join(base_path, "measuring_vid" + str(index) + ".mp4")
    out = cv2.VideoWriter(videoPath, fourcc, 20.0, (frame_width, frame_height))

    while True:
        ret, frame = cam.read()

        if ret:
            # Write the frame to the output file
            out.write(frame)

            # Display the captured frame
            cv2.imshow('Camera', frame)

            # Press 'q' to exit the loop
            if cv2.waitKey(1) == ord('q'):
                break
        
        else:
            print("Failed to capture frame")

    # Release the capture and writer objects
    cam.release()
    out.release()
    cv2.destroyAllWindows()

    undistortedVideoPath = undistortCameras.undistort(videoPath, os.path.join(base_path, "measuring_vid_undistorted" + str(index) + ".mp4"))
    return undistortedVideoPath        # return the path to the video file for later use in image processing

if __name__ == "__main__":
    take_video()