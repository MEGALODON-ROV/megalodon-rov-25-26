import cv2
import os
import undistortCameras

def take_video(camIndex=1):
    base_path = os.path.dirname(__file__)

    # Open the robot's camera
    cam = cv2.VideoCapture(camIndex, cv2.CAP_DSHOW)        # use cv2.CAP_DSHOW to tell openCV
                                                    # to use camera driver backend
                                                    # instead of default backend

    # Get the default frame width and height
    frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    crop_width = int(frame_width * 3/5)     # crop to middle 3/5 of the width
    crop_height = int(frame_height * 1/2)   # crop to middle 1/2 of the height

    # Define the codec and create VideoWriter object. 
    # For the VideoWriter func, may have to switch path.
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # find new file to write still-distorted video into
    index = 0
    videoPath = os.path.join(base_path, "measuring_vid" + str(index) + ".mp4")
    while os.path.exists(videoPath):
        index += 1
        videoPath = os.path.join(base_path, "measuring_vid" + str(index) + ".mp4")
    out = cv2.VideoWriter(videoPath, fourcc, 20.0, (crop_width, crop_height))

    print("Recording video. Press 'q' to stop recording.")

    while True:
        ret, frame = cam.read()

        if ret:
            # Display the captured frame
            cv2.imshow('Camera', frame)

            # crop the frame to start from 1/5 way to 4/5 way horizontally, and 1/4 way to 3/4 way vertically
            # need to crop because camera feed is covered at edges by ROV
            frame = frame[int(frame_height/4):int(3*frame_height/4), int(frame_width/5):int(4*frame_width/5)]
            # Write the frame to the output file
            out.write(frame)

            # Display the cropped frame
            cv2.imshow('Cropped', frame)

            # Press 'q' to exit the loop
            if cv2.waitKey(1) == ord('q'):
                break
        
        else:
            print("Failed to capture frame")

    # Release the capture and writer objects
    cam.release()
    out.release()
    cv2.destroyAllWindows()

    undistortedVideoPath = os.path.join(base_path, "measuring_vid_undistorted" + str(index) + ".mp4")

    undistortCameras.undistort(videoPath, undistortedVideoPath)
    return undistortedVideoPath        # return the path to the video file for later use in image processing

if __name__ == "__main__":
    take_video()