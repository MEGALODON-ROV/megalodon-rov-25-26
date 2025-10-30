import cv2


#connect to deafult camera
cam = cv2.VideoCapture(0)
#find width and height of live feed
width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT)) 

#define the codec 
FOURCC = cv2.VideoWriter_fourcc(*'mp4v') #compress mp4v
output = cv2.VideoWriter('output.mp4', FOURCC, 20.0, (width, height))

#read frames
while True:
    ret, frame = cam.read() #read frames
    output.write(frame) #write frames into output file
    cv2.imshow('Camera', frame) #show live feed

    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'): # press s to capture snapshot
        cv2.imwrite('snapshot.png', frame)
        print("Snapshot saved as snapshot.png")

    if key == ord('q'): #press q to quit
        break





#release camera and output
cam.release()
output.release()
cv2.destroyAllWindows()

