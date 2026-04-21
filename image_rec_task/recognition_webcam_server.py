import cv2
import socket
import struct

# Open webcam
cap = cv2.VideoCapture(0)

# Create TCP server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 9999))
server_socket.listen(1)

print("Waiting for WSL client to connect...")
conn, addr = server_socket.accept()
print("Connected:", addr)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # Reduce resolution for smoother streaming
    frame = cv2.resize(frame, (640, 480))

    # Encode frame as JPEG
    _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
    data = buffer.tobytes()

    # Send header (4 bytes) + frame
    header = struct.pack("!I", len(data))
    conn.sendall(header + data)
