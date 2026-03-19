import cv2
import numpy as np
# import os
import glob     # for easier file searching

def calibrate_camera():
    # Defining the dimensions of checkerboard
    CHECKERBOARD = (6,9)        # change
    # criteria for termination of the iterative process of corner refinement
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
                                                    # stop after 30 iterations
                                                    # or when corner changes by
                                                    # less than 0.001

    # vectors can change sizes
    # these 2 arrays establish relationship between world and image points
    # Creating vector to store vectors of 3D points for corners in each checkerboard image
        # are world coordinates of the checkerboard corners
    objpoints = []
    # Creating vector to store vectors of 2D points for corners in each checkerboard image
        # are coordinates distorted by the camera lens
    imgpoints = []


    # Defining the world coordinates for 3D points
    objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
                                                # create matrix of zeros with dimensions
                                                # 1 for 1 image
                                                # CHECKERBOARD[0] * CHECKERBOARD[1]
                                                    # for number of inner corners on CHECKERBOARD
                                                # 3 for 3D coordinates (X, Y, Z)
    objp[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
                                        # create a mesh grid of points for 2 arrays
                                            # [0, CHECKERBOARD[0]) filled with x-coords
                                            # [0, CHECKERBOARD[1]) filled with y-coords
                                            # shape is (2, CHECKERBOARD[0], CHECKERBOARD[1])
                                        # transpose to shape (CHECKERBOARD[0], CHECKERBOARD[1], 2)
                                        # reshape to (CHECKERBOARD[0] * CHECKERBOARD[1], 2)
                                            # -1 means to automatically calculate the dimension
                                        # assign this to first two columns of objp
                                            # last column in objp remains 0 (Z-coord)
                                                # because 2 is not included in :2 slice

    # Extracting path of individual image stored in a given directory
    # images of checkerboard taken by camera to be calibrated!
    images = glob.glob('./images/*.jpg')        # all .jpg files in images/ folder
    for fileName in images:
        img = cv2.imread(fileName)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        # If desired number of corners are found in the image then ret = true
        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
                                                # what the flags do:
                                                    # adaptive threshholding for varying
                                                        # lighting conditions
                                                    # reject images w/o a checkerboard
                                                    # normalize image brightness
                                                        # before processing

        
        """
        If desired number of corner are detected (good image!),
        we refine the pixel coordinates and display
        them on the images of checker board
        """
        if ret == True:
            objpoints.append(objp)
            # refining pixel coordinates for given 2d points (sub-pixel precision!)
                # for better calibration accuracy
            corners2 = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
                                    # (11,11) is the search window size around each corner
                                    # (-1, -1) indicates that there is no dead zone
                                        # in the center of the search window
            
            imgpoints.append(corners2)
    
            # Draw and display the corners
            # img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
        
        # cv2.imshow('img',img)
        # cv2.waitKey(0)
    
    # cv2.destroyAllWindows()
    
    h, w = img.shape[:2]
    
    """
    Performing camera calibration by 
    passing the value of known 3D points (objpoints)
    and corresponding pixel coordinates of the 
    detected corners (imgpoints)
    """
    reproj, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        # reproj: reprojection error - how well the calibration worked, lower = better
        # mtx: 3 x 3 camera matrix - intrinsic parameters
            # [[fx,  0, cx],
            # [ 0, fy, cy],
            # [ 0,  0,  1]]
            # fx, fy: focal lengths in pixels along x and y axes
            # cx, cy: optical centers (usually near image center)
            # 1 is multiplied onto z to make matrix multiplication work
        # dist: array of lens distortion coefficients
        # rvecs: list of rotation of checkerboard
            # relative to camera vectors (one per image)
        # tvecs: list of translation of checkerboard
            # relative to camera vectors (one per image)
            # each vector is [x, y, z] distance
                # from optical center to checkboard's origin in world units
    
    print("rvecs: \n{}".format(rvecs))
    print("tvecs: \n{}".format(tvecs))
    print("Camera matrix: \n{}".format(mtx))
    print("dist: \n{}".format(dist))
    print("w: {}, h: {}".format(w, h))
    return mtx, dist, w, h