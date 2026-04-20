import cv2
import socket
import struct
import numpy as np
import threading
import time
from ultralytics import YOLO

# Load YOLO model
model = YOLO("CRAB_4FIN.pt")

# Connect to Windows server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("172.29.64.1", 9999))

data = b""
payload_size = struct.calcsize("!I")

cv2.namedWindow("YOLO Detection", cv2.WINDOW_NORMAL)
cv2.resizeWindow("YOLO Detection", 640, 480)

latest_frame = None
latest_annotated = None
latest_crab_count = 0
lock = threading.Lock()

CRAB_CLASS_ID = 0  # European Green Crab

def yolo_thread():
    global latest_frame, latest_annotated, latest_crab_count
    while True:
        with lock:
            if latest_frame is None:
                time.sleep(0.001)
                continue
            frame_copy = latest_frame.copy()

        # Run YOLO on full resolution
        results = model.predict(
            frame_copy,
            conf=0.05,   # lower threshold
            imgsz=960,   # higher resolution
            verbose=False
        )

        # Keep ONLY European Green Crab (class 0)
        mask = [int(c) == CRAB_CLASS_ID for c in results[0].boxes.cls]
        results[0].boxes = results[0].boxes[mask]

        # YOLO draws its own boxes + labels + confidence
        annotated = results[0].plot()

        # Count crabs
        crab_count = len(results[0].boxes)

        with lock:
            latest_annotated = annotated.copy()
            latest_crab_count = crab_count

        time.sleep(0.001)

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

    with lock:
        latest_frame = frame

    with lock:
        display_frame = latest_annotated if latest_annotated is not None else frame
        count = latest_crab_count

    # Draw crab count
    cv2.putText(
        display_frame,
        f"European Green Crabs: {count}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 255, 0),
        2
    )

    cv2.imshow("YOLO Detection", display_frame)
    if cv2.waitKey(1) == 27:
        break

client_socket.close()
