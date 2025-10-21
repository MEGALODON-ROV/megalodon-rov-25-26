import cv2
import os
import numpy as np

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
