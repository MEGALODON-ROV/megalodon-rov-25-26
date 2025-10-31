import cv2
import os
import numpy as np
import imutils
import matplotlib.pyplot as plt

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


# DRAWING ON IMAGES SECTION
# to draw a line: cv2.line(image, startPoint (tuple), endPoint (tuple), color(BGR), thickness)
# to draw a rectangle need top-left and bottom-right points
# for circle need center point and radius
# for a polygon, make an array of points, reshape it to a (-1, 1, 2) and use cv2.polylines()
    # np will calculate -1 based on array size
    # 1 is num of polygons
    # 2 is coordinates per point (x, y)
#draw a rectangle around Trump's head and label it
imageToDrawOn = cv2.imread(os.path.join(base_path, "trumpFunny.jpg"), cv2.IMREAD_COLOR)
copiedImage = imageToDrawOn.copy()
cv2.rectangle(imageToDrawOn, (250, 0), (400, 300), (0, 255, 0), 5)   # green rectangle w/ thickness 5px
font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
cv2.putText(imageToDrawOn, "Trump's Head", (0, 310), font, 3, (0, 0, 0), 2, cv2.LINE_AA)
cv2.imshow("Labeled Trump", imageToDrawOn)
# experiment with using polylines
points = np.array([[250,0], [400,0], [400,300], [250,300]])
points = points.reshape(-1, 1, 2)
cv2.polylines(copiedImage, [points], isClosed = True, color = (0, 255, 0), thickness = 5)
cv2.imshow("Polylines Trump", copiedImage)
cv2.waitKey(0)
cv2.destroyAllWindows()


# CONTOURS SECTION
trump = cv2.imread(os.path.join(base_path, "trumpFunny.jpg"), cv2.IMREAD_COLOR)
trump = trump[0:800, 0:460]
gray = cv2.imread(os.path.join(base_path, "trumpFunny.jpg"), cv2.IMREAD_GRAYSCALE)
gray = gray[0:800, 0:460]
_, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)   # thresholding to get < 100 turn off, > 100 turn on
cv2.imshow("Binary Image", binary)

# hierarchy: tells when there are contours inside contours
# RETR_EXTERNAL: only get outer contours (not only largest)
# RETR_TREE: get all contours and create a full hierarchy
# CHAIN_APPROX_SIMPLE: how to get the contours
contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
draw = cv2.drawContours(trump, contours, -1, (50, 150, 255), 5)   # -1 means draw all contours
cv2.imshow("Contours", draw)

largestContour = max(contours, key = cv2.contourArea)   # get the largest contour by area
approxConts = trump.copy()
length = cv2.arcLength(largestContour, True)   # True means contour is closed
approx = cv2.approxPolyDP(largestContour, 0.005 * length, True)
cv2.drawContours(approxConts, [approx], -1, (0, 255, 0), 5)
cv2.imshow("Approximated Contours", approxConts)
cv2.waitKey(0)
cv2.destroyAllWindows()


# SHAPE DETECTION SECTION
# basics of shape detection:
    # blur the grayscaled and thresholded image to reduce noise
    # do contour approximation (find largest contour, approxPolyDP)
    # use length of the returned list of edges of shape to determine # edges
    # use # edges to find shape type

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, contour):
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)

        if len(approx) == 3:
            return "triangle"
        elif len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ratio = w / float(h)
            if ratio >= 0.95 and ratio <= 1.05:
                return "square"
            else:
                return "rectangle"
        elif len(approx) == 5:
            return "pentagon"
        else:
            return "circle"     # assume as circle if more than 5 edges

# get image and resize for easier processing
shapes = cv2.imread(os.path.join(base_path, "geometricShapes.jpg"), cv2.IMREAD_COLOR)
#resized = cv2.resize(shapes, (300, 300))
#ratio = shapes.shape[0] / float(resized.shape[0])

# blur to get rid of noise
gray = cv2.cvtColor(shapes, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
_, thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)

# find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# find shapes
shapeDetector = ShapeDetector()
for contour in contours: # go through the contour of each shape found
    #find center of contour for labeling
    moment = cv2.moments(contour)
    if moment["m00"] == 0:      # avoid division by 0
        continue
    cX = int((moment["m10"] / moment["m00"]) * ratio)
    cY = int((moment["m01"] / moment["m00"]) * ratio)

    # find the shape
    shape = shapeDetector.detect(contour)

    # convert contour from object into usable type
    #contour = contour.astype("float")
    #contour *= ratio
    contour = contour.astype("int")

    # draw on the shapes and labels
    cv2.drawContours(shapes, [contour], -1, (0, 255, 0), 2)
    cv2.putText(shapes, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 0, 0), 2)
    

# show the output image
cv2.imshow("Detected Shapes", shapes)
cv2.waitKey(0)
cv2.destroyAllWindows()