import cv2
import calibrateCameras as calib
import glob

# probs need to change to have 1 file for calibration images
# and another for actual images we need to undistort
# so we don't recalibrate every time
# in future also just calibrate once,
    # take note of the values,
    # and hardcode them into the undistortion script
images = glob.glob('./images/*.jpg')  # all .jpg files in /images/ folder
        # "./" means current directory
mtx, dist, w, h = calib.calibrate_camera()

# Refining the camera matrix using parameters obtained by calibration
# to maximize FOV after undistortion since undistorting causes black borders
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 0, (w,h))
                    # mtx is the original camera matrix from calibration
                    # dist is the distortion coefficients from calibration
                    # (w,h) is the size of the image
                    # 0 means remove all black pixels (no black borders)
                        # cv2 predicts where black borders will be and zooms in accordingly
                    # (w,h) is the new image size
                    # newcameramtx is the refined camera matrix
                    # roi is region of interest (without any removed black borders)

# Method 1 to undistort the image
mapx, mapy=cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)
            # calculate processing for many images once
            # mapping computed once then reused


for fileName in images:
    img = cv2.imread(fileName)

    # Method 2 to undistort the image
    # dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
            # does both steps on initUndistortRectifyMap + remap in one step
            # slower, esp for videos
    
    undistortedImage = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
            # map the distorted image with
            # precomputed maps to undistort the image
    
    # Displaying the undistorted image
    cv2.imshow("undistorted image", undistortedImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()