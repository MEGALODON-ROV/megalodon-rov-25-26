# file to take pictures of checkers board and save them to the images folder
# for camera calibration
import cv2
import os

def takePic():
    # create images folder if it doesn't exist
    if not os.path.exists('calibration_images'):
        os.makedirs('calibration_images')

    # wipe all images in the images folder to avoid confusion with old calibration images
    for filename in os.listdir('calibration_images'):
        file_path = os.path.join('calibration_images', filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # open camera
    cap = cv2.VideoCapture(0)

    while True:
        # read frame from camera
        ret, frame = cap.read()

        # display the frame
        cv2.imshow('frame', frame)

        # wait for key press
        key = cv2.waitKey(3) & 0xFF

        # if 's' is pressed, save the image
        if key == ord('s'):
            img_name = f"calibration_images/checkers_{len(os.listdir('calibration_images'))}.jpg"
            cv2.imwrite(img_name, frame)
            print(f"Image saved: {img_name}")

        # if 'q' is pressed, exit the loop
        elif key == ord('q'):
            break

    # release the camera and close windows
    cap.release()
    cv2.destroyAllWindows()