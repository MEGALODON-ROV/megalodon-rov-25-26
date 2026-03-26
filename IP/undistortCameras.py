import cv2
import IP.calibrateCameras as calib
import glob

def undistort(input_video_path, output_video_path):
    # probs need to change to have 1 file for calibration images
    # and another for actual images we need to undistort
    # so we don't recalibrate every time
    # in future also just calibrate once,
    # take note of the values,
    # and hardcode them into the undistortion script
    images = glob.glob('./images/*.jpg')  # all .jpg files in /images/ folder
        # "./" means current directory
    mtx, dist, w, h = calib.calibrate_camera()
        # w and h are the width and height of the images used for calibration

    # open input video
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    # read video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30.0  # default to 30 fps if unable to get fps from video
    # width and height of current video frames
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


    # Refining the camera matrix using parameters obtained by calibration
    # to maximize FOV after undistortion since undistorting causes black borders
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (frame_width, frame_height), 0, (frame_width, frame_height))
                # mtx is the original camera matrix from calibration
                # dist is the distortion coefficients from calibration
                # (frame_width, frame_height) is the size of the image
                # 0 means remove all black pixels (no black borders)
                # cv2 predicts where black borders will be and zooms in accordingly
                # (frame_width, frame_height) is the new image size
                # newcameramtx is the refined camera matrix
                # roi is region of interest (without any removed black borders)

    # Method 1 to undistort the image
    mapx, mapy=cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (frame_width, frame_height), 5)
        # calculate processing for many images once
        # mapping computed once then reused

    # undistort each frame of the video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # codec for mp4
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    if not out.isOpened():
        cap.release()
        print("Error: Could not open video writer.")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # end of video
        undistortedFrame = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
        out.write(undistortedFrame)
    
    cap.release()
    out.release()

    return output_video_path