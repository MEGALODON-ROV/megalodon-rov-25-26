from email.mime import image
import cv2
import os
import numpy as np
import imutils

base_path = os.path.dirname(__file__)

# # TRUMP IMAGE SECTION
# trump_path = os.path.join(base_path, "trumpFunny.jpg")
# trump = cv2.imread(trump_path, cv2.IMREAD_COLOR)
# # trump = cv2.imread(os.path.abspath(__file__) + "\..\\trumpFunny.jpg", cv2.IMREAD_COLOR)   # this also works but is evil
# cv2.imshow("My Image", trump)
# cv2.waitKey(0)      # waits for 0 ms to check if user pressed a key
# cv2.destroyAllWindows()
# cv2.imwrite(os.path.join(os.path.dirname(__file__), "trumpCopy.jpg"), trump)

# # CAMERA SECTION
# camera = cv2.VideoCapture(0)    # 0 is usually the built-in webcam

# # dimentions of the camera feed
# width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

# # codec = device/program that compresses data for faster transmission and
# # decompresses data for receiving
# # define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # four character code saying how to encode/decode video
# outputFile = cv2.VideoWriter(os.path.join(base_path, "camOutput.mp4"), fourcc, 20.0, (width, height)) # 20.0 is fps, output.mp4
#                                                                           # is name of saved video file

# while True:
#     captured, frame = camera.read()   # read() returns 2 values, first is boolean
#                                       # saying if frame was captured successfully

#     # write frame to the output file
#     if captured:
#         outputFile.write(frame)
#         cv2.imshow("Camera Feed", frame)   # display the frame in a window

#     # press "q" to exit loop
#     if cv2.waitKey(1) == ord("q"):
#         break
#     if cv2.waitKey(1) == ord("s"):
#         beginNum = 0
#         while os.path.exists(os.path.join(base_path, "capturedImage"+str(beginNum)+".jpg")):
#             beginNum += 1
#         cv2.imwrite(os.path.join(base_path, "capturedImage"+str(beginNum)+".jpg"), frame)
#         print("Image saved!")

# # release the capture and writer objects and close any open windows
# camera.release()
# outputFile.release()
# cv2.destroyAllWindows()

# CROPPING IMAGE SECTION
# croppedImage = image[startY:endY, startX:endX]

imageToCrop = cv2.imread(os.path.join(base_path, "trumpFunny.jpg"), cv2.IMREAD_COLOR)
cv2.imshow("Original Image", imageToCrop)
print(imageToCrop.shape)        # prints (rows, columns, color channels)
croppedImage = imageToCrop[0:300, 250:400]      # trump's head!!!
cv2.imshow("Cropped Image", croppedImage)
cv2.waitKey(0)
cv2.destroyAllWindows()

# RESIZING IMAGE SECTION
# resize image width to 150 pixels, keep aspect ratio
ratio = 150 / imageToCrop.shape[1]      # newWidth / oldWidth
dimension = (150, int(ratio * imageToCrop.shape[0]))    # width, height aka y, x
resizedImage = cv2.resize(imageToCrop, dimension, interpolation=cv2.INTER_AREA)
cv2.imshow("Width Resized Image", resizedImage)

# resize image to height of 50 pixels
ratio = 50 / imageToCrop.shape[0]      # newHeight / oldHeight
dimension = (int(ratio * imageToCrop.shape[1]), 50)
resizedImage2 = cv2.resize(imageToCrop, dimension, interpolation=cv2.INTER_AREA)
cv2.imshow("Height Resized Image", resizedImage2)

# use imutils to resize image
resizedImage3 = imutils.resize(imageToCrop, width = 150)
cv2.imshow("Imutils Width Resized Image", resizedImage3)
resizedImage4 = imutils.resize(imageToCrop, height = 50)
cv2.imshow("Imutils Height Resized Image", resizedImage4)

# half of width and height
resizedImage5 = imutils.resize(imageToCrop, width = int(imageToCrop.shape[1] / 2))
cv2.imshow("Half Resized Image", resizedImage5)
cv2.waitKey(0)
cv2.destroyAllWindows()

# notes on interpolation methods:
# cv2.INTER_NEAREST: fast, takes neightbor pixel value and assumes intensity (bad quality)
# cv2.INTER_LINEAR: default, calculates pixels with y=mx+b (highest quality for speed)
# cv2.INTER_AREA: good for shrinking images, may be slower
# cv2.INTER_CUBIC: better but slower (complicated lol, can upsample too)
# cv2.INTER_LANCZOS4: best but slowest (not often used)

# CONCATENATING IMAGES SECTION
# concatenate images of different widths
def vconcat_resize(img_list, interpolation = cv2.INTER_LINEAR):
    # get the smaller width
    w_min = min(image.shape[1] for image in img_list)

    # resize images to the smaller width and store them in a new list
    im_list_resize = [imutils.resize(image, width = w_min, inter = interpolation) for image in img_list]

    return cv2.vconcat(im_list_resize)

def hconcat_resize(img_list, interpolation = cv2.INTER_LINEAR):
    # get the smaller height
    h_min = min(image.shape[0] for image in img_list)

    # resize images to the smaller height and store them in a new list
    im_list_resize = [imutils.resize(image, height = h_min, inter = interpolation) for image in img_list]

    return cv2.hconcat(im_list_resize)

def concat_2D_resize(img_list_2D, interpolation = cv2.INTER_LINEAR):
    # resize to have same height so that we can concatenate each hori line of 2D list
    # and then concatenate each hori line so that it is ready to be concatenated vertically
    im_list_2D_resize = [hconcat_resize(im_list, interpolation = interpolation) for im_list in img_list_2D]

    return vconcat_resize(im_list_2D_resize, interpolation = interpolation)

# try calling the function!
image1 = cv2.imread(os.path.join(base_path, "trumpFunny.jpg"), cv2.IMREAD_COLOR)
image2 = cv2.imread(os.path.join(base_path, "bidenFunny.jpg"), cv2.IMREAD_COLOR)

vert_concat_image = vconcat_resize([image1, image2])
cv2.imshow("Vertical Concatenation", vert_concat_image)
horiz_concat_image = hconcat_resize([image1, image2])
cv2.imshow("Horizontal Concatenation", horiz_concat_image)
grid_concat_image = concat_2D_resize([[image1, image2], [image1, image2, image1], [image2]])
cv2.imshow("Grid Concatenation", grid_concat_image)
cv2.waitKey(0)
cv2.destroyAllWindows()