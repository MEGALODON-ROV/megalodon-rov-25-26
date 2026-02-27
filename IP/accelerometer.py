import serial
import numpy as np
import time
import matplotlib.pyplot as plt

cereal = serial.Serial("/dev/cu.usbmodem1101", 115200, timeout=1)   # change to your port if needed

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

    complete = line.__contains__(":done") and line.__contains__("start+")

    if not complete:
        print("bad data")
        extract()
    else:

        #print("Raw data: " + line)

        try:
            data, done = line.split(":")
            start, data2 = data.split("+")
            xy, z_str = data2.split(';')
            x_str, y_str = xy.split(',')

            global x, y, z
            x = float(x_str)
            y = float(y_str)
            z = float(z_str)

            #print(x_str + ", " + y_str + ", " + z_str)
        except ValueError:
            pass

def average(axis):
    clock = 0
    holding = 0
    while clock < 500:
        clock +=1
        extract()
        if axis == "x":
            holding += x
        if axis == "y":
            holding += y
        if axis == "z":
            holding += z
    return holding / 500

# calibrating!
# positions: +X, -X, +Y, -Y, +Z, -Z
# X CALIBRATION
extract()

input("Flip to +x side and press enter when ready)")
temp = average("x")

input("Flip to -x side and press enter when ready")
temp2 = average("x")

xerr = (temp + temp2) / 2
xscl = 9.81 / ((temp - temp2) / 2)

# Y CALIBRATION
input("Flip to +y side and press enter when ready")
temp = average("y")

input("Flip to -y side and press enter when ready")
temp2 = average("y")

yerr = (temp + temp2) / 2
yscl = 9.81 / ((temp - temp2) / 2)

# Z CALIBRATION
input("Flip to +z side and press enter when ready")
temp = average("z")

input("Flip to -z side and press enter when ready")
temp2 = average("z")

zerr = (temp + temp2) / 2
zscl = 9.81 / ((temp - temp2) / 2)

# print calibration results
print("xerr: " + str(xerr) + ", xscl: " + str(xscl) + "\n")
print("yerr: " + str(yerr) + ", yscl: " + str(yscl) + "\n")
print("zerr: " + str(zerr) + ", zscl: " + str(zscl) + "\n")

velocity = [0, 0, 0]  # vx, vy, vz
position = [0, 0, 0]  # px, py, pz
# apply error and scale values to get calibrated values
acceleration = np.empty((0, 4), float) # ax, ay, az, time

time.sleep(10)

startingSeconds = time.time()

# TEMP TESTING CODE CHANGE LOOPING CONDITION BACK TO TRUE LATER
clock = 0
while clock < 90000:    # 15 minutes at 100Hz
    extract()       # get current accel reading
    xCalib = (x - xerr) * xscl  # change to correct calibrated value lol
    yCalib = (y - yerr) * yscl
    zCalib = (z - zerr) * zscl
    if clock % 1000 == 0:
        acceleration = np.append(acceleration, [[xCalib, yCalib, zCalib, time.time() - startingSeconds]], axis=0)

    # integrate to get velocity
    velocity[0] += (xCalib / 100)
    velocity[1] += (yCalib / 100)
    velocity[2] += ((zCalib - 9.81) / 100 )
    # integrate to get position
    position[0] += (velocity[0] / 100)
    position[1] += (velocity[1] / 100)
    position[2] += (velocity[2] / 100)

    #print(str(xCalib) + ", " + str(yCalib) + ", " + str(zCalib))
    print(str(round(position[0])) + ", " + str(round(position[1])) + ", " + str(round(position[2])))
    time.sleep(0.01) # same delay as in arduino code
    clock += 1

# graph x acceleration data
plt.plot(acceleration[:, 3], acceleration[:, 0])
plt.xlabel('Time (s)')
plt.ylabel('X Acceleration (m/s^2)')
plt.title('X Acceleration vs Time')

# graph y acceleration data
plt.figure()
plt.plot(acceleration[:, 3], acceleration[:, 1])
plt.xlabel('Time (s)')
plt.ylabel('Y Acceleration (m/s^2)')
plt.title('Y Acceleration vs Time')

# graph z acceleration data
plt.figure()
plt.plot(acceleration[:, 3], acceleration[:, 2])
plt.xlabel('Time (s)')
plt.ylabel('Z Acceleration (m/s^2)')
plt.title('Z Acceleration vs Time')
plt.show()