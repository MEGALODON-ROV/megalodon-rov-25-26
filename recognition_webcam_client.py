import cv2
import socket
import struct
import numpy as np
import threading
import time
from ultralytics import YOLO

# Load YOLO model
model = YOLO("CRAB_4FIN.pt")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("172.29.64.1", 9999))

data = b""
payload_size = struct.calcsize("!I")

cv2.namedWindow("YOLO Detection", cv2.WINDOW_NORMAL)
cv2.resizeWindow("YOLO Detection", 640, 480)

latest_frame = None
latest_annotated = None
lock = threading.Lock()

def yolo_thread():
    global latest_frame, latest_annotated
    while True:
        # Grab the latest frame safely
        with lock:
            if latest_frame is None:
                time.sleep(0.001)
                continue
            frame_copy = latest_frame.copy()

        # Downscale for faster YOLO inference
        small = cv2.resize(frame_copy, (320, 240))

        # Run YOLO on the smaller frame
        results = model.predict(small, verbose=False)
        annotated_small = results[0].plot()

        # Upscale back to original size
        annotated = cv2.resize(
            annotated_small,
            (frame_copy.shape[1], frame_copy.shape[0])
        )

        # Store the annotated frame
        with lock:
            latest_annotated = annotated.copy()

        time.sleep(0.001)  # stabilize CPU scheduling

# Start YOLO thread
threading.Thread(target=yolo_thread, daemon=True).start()

while True:
    # Receive header
    while len(data) < payload_size:
        packet = client_socket.recv(4096)
        if not packet:
            break
        data += packet

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("!I", packed_msg_size)[0]

    # Receive JPEG frame bytes
    while len(data) < msg_size:
        data += client_socket.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    # Decode JPEG → BGR
    frame = cv2.imdecode(
        np.frombuffer(frame_data, dtype=np.uint8),
        cv2.IMREAD_COLOR
    )

    # Update YOLO thread with latest frame
    with lock:
        latest_frame = frame

    # Display YOLO output if available, otherwise raw frame
    with lock:
        display_frame = latest_annotated if latest_annotated is not None else frame

    cv2.imshow("YOLO Detection", display_frame)
    if cv2.waitKey(1) == 27:
        break

client_socket.close()
