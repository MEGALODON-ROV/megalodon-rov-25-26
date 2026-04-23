import serial
import time

cereal = serial.Serial("/dev/cu.usbserial-10", 9600, timeout=10)
# Change the port as needed (ex. if Windows, COM3 or something like that)

FACTOR = 1.004288867 # depth sent by sensor to actual depth
OFFSET = 0.161498

def extract():
    cereal.reset_input_buffer()  # Clear old data that builds up in queue
    line = cereal.readline().decode('utf-8').strip()

    complete = line.__contains__("s+") and line.__contains__("-e")

    if not complete:
        print("bad data")
        extract()
    else:

        #print("Raw data: " + line)

        try:
            _, leftover = line.split("+")
            data, _ = leftover.split("-")
        except ValueError:
            pass
    if complete:
        return (float(data) * FACTOR) + OFFSET

if __name__ == "__main__":
    while True:
        print(extract())
        time.sleep(0.2)