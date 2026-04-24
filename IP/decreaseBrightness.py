import glob
import cv2
import random

images = glob.glob('./trainingPics/*.jpeg')        # all .jpeg files in /trainingPics/ folder

for img in images:
    # make every image more "gloomy" by decreasing brightness by a random int
    image = cv2.imread(img)
    brightness_decrease = random.randint(30, 70)
    gloomy_img = cv2.convertScaleAbs(image, alpha=1.1, beta=-brightness_decrease)

    # save gloomy image into darkenedImgs folder
    save_path = img.replace('trainingPics', 'darkenedImgs')
    cv2.imwrite(save_path, gloomy_img)