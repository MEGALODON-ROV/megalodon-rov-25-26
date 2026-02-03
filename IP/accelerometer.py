import cv2
import serial
from time import sleep

cereal = serial.Serial("COM12", 9600, timeout=1)

x = 0
y = 0
z = 0
temp = 0
xerr = 0
xscl = 0
yerr = 0
yscl = 0
zerr = 0
zscl = 0

def extract():
    cereal.reset_input_buffer()  # Clear old data that builds up in queue
    line = cereal.readline().decode('utf-8').strip()
    print("Raw data: " + line)

    try:
        xy, z_str = line.split(';')
        x_str, y_str = xy.split(',')

        global x, y, z
        x = float(x_str)
        y = float(y_str)
        z = float(z_str)

        print(x_str + ", " + y_str + ", " + z_str)
    except ValueError:
        pass

# clock = 0
#
# while clock < 100:
#     extract()
#     sleep(0.1)
#     clock += 1

# calibrating!
# X CALIBRATION
input("flip to +x side and press enter when ready)")
extract()
temp = x
print("tempx: " + str(temp) + " ")

input("flip to -x side and press enter when ready")
while x == temp:    # accounts for divide by 0
    extract()
    sleep(0.01)
print("negx: " + str(x) + "\n")

xerr = (temp + x) / 2
xscl = 9.81 / ((temp - x) / 2)

# Y CALIBRATION
input("flip to +y side and press enter when ready")
extract()
temp = y
print("tempy: " + str(temp) + " ")

input("flip to -y side and press enter when ready")
while y == temp:
    extract()
    sleep(0.01)
print("negy: " + str(y) + "\n")

yerr = (temp + y) / 2
yscl = 9.81 / ((temp - y) / 2)

# Z CALIBRATION
input("flip to +z side and press enter when ready")
extract()
temp = z
print("tempz: " + str(temp) + " ")

input("flip to -z side and press enter when ready")
while z == temp:
    extract()
    sleep(0.01)
print("negz: " + str(z) + "\n")

zerr = (temp + z) / 2
zscl = 9.81 / ((temp - z) / 2)

# print calibration results
print("xerr: " + str(xerr) + ", xscl: " + str(xscl) + "\n")
print("yerr: " + str(yerr) + ", yscl: " + str(yscl) + "\n")
print("zerr: " + str(zerr) + ", zscl: " + str(zscl) + "\n")

velocity = [0, 0, 0]  # vx, vy, vz
position = [0, 0, 0]  # px, py, pz
# apply error and scale values to get calibrated values
while True:
    extract()       # get current accel reading
    xCalib = (x - xerr) * xscl  # change to correct calibrated value lol
    yCalib = (y - yerr) * yscl
    zCalib = (z - zerr) * zscl

    # integrate to get velocity
    velocity[0] += xCalib
    velocity[1] += yCalib
    velocity[2] += zCalib
    # integrate to get position
    position[0] += velocity[0]
    position[1] += velocity[1]
    position[2] += velocity[2]

    print(str(xCalib) + ", " + str(yCalib) + ", " + str(zCalib))
    sleep(0.1)      # same delay as in arduino code

#positions: +X, -X, +Y, -Y, +Z, -Z