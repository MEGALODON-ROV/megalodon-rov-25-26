import serial
import numpy as np
import time
import matplotlib.pyplot as plt

print("start")

# execute immediately
cereal = serial.Serial("/dev/cu.usbmodem11301", 115200, timeout=1)   # change to your port if needed

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
smoother1 = 0
smoother2 = 0
smoother3 = 0
smoother4 = 0
smoother5 = 0

# velocity and position lists for graphing and position tracking
velocity = [0, 0, 0]  # vx, vy, vz
position = [0, 0, 0]  # px, py, pz
# numpy arrays for graphing
acceleration = np.empty((0, 4), float) # ax, ay, az, time
vel_graphing = np.empty((0, 4), float) # vx, vy, vz, time
dist_graphing = np.empty((0, 4), float) # px, py, pz, time

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
            data, _ = line.split(":")
            _, data2 = data.split("+")
            xy, z_str = data2.split(';')
            x_str, y_str = xy.split(',')

            global x, y, z
            x = float(x_str)
            y = float(y_str)
            z = float(z_str)

            #print(x_str + ", " + y_str + ", " + z_str)
        except ValueError:
            pass

def smoothedExtract():
    global smoother1, smoother2, smoother3, smoother4, smoother5
    smoother1 = smoother2
    smoother2 = smoother3
    smoother3 = smoother4
    smoother4 = smoother5
    smoother5 = extract()
    avg = (smoother1 + smoother2 + smoother3 + smoother4 + smoother5) / 5
    return avg

def average(axis):
    clock = 0
    holding = 0
    while clock < 1000:
        clock +=1
        extract()
        if axis == "x":
            holding += x
        elif axis == "y":
            holding += y
        elif axis == "z":
            holding += z
    return holding / 1000

# calibrating!
# positions: +X, -X, +Y, -Y, +Z, -Z
def calibrate():
    # X CALIBRATION
    #extract() seems to be unnecessary since we're not using the accel data here???
    global xerr, xscl, yerr, yscl, zerr, zscl

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

def trackPosition():
    global velocity, position, acceleration, vel_graphing, dist_graphing

    # TEMP TESTING CODE CHANGE LOOPING CONDITION BACK TO TRUE LATER
    startingSeconds = time.time()
    clock = 0   # TEMPORARY, for testing
    while clock < 6000:    # 1 minute at 100Hz 
                            # It actually works out to 140 seconds or so for some reason
        smoothedExtract()       # get current accel reading
        xCalib = (x - xerr) * xscl  # change to correct calibrated value lol
        yCalib = (y - yerr) * yscl
        zCalib = (z - zerr) * zscl

        # integrate to get velocity
        velocity[0] += (xCalib / 100)
        velocity[1] += (yCalib / 100)
        velocity[2] += ((zCalib - 9.81) / 100 )
        # integrate to get position
        position[0] += (velocity[0] / 100)
        position[1] += (velocity[1] / 100)
        position[2] += (velocity[2] / 100)

        if clock % 100 == 0:    # TEMPORARY, for testing
            acceleration = np.append(acceleration, [[xCalib, yCalib, zCalib, time.time() - startingSeconds]], axis=0)
            vel_graphing = np.append(vel_graphing, [[velocity[0], velocity[1], velocity[2], time.time() - startingSeconds]], axis=0)
            dist_graphing = np.append(dist_graphing, [[position[0], position[1], position[2], time.time() - startingSeconds]], axis=0)

        #print(str(xCalib) + ", " + str(yCalib) + ", " + str(zCalib))
        print(str(round(position[0])) + ", " + str(round(position[1])) + ", " + str(round(position[2])))
        time.sleep(0.01) # same delay as in arduino code
        clock += 1  # TEMPORARY, for testing
    
    graphAll()      # TEMPORARY, for testing

def graphAll():
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

    # graph velocity data
    plt.figure()
    plt.plot(vel_graphing[:, 3], vel_graphing[:, 0], label='Vx')
    plt.plot(vel_graphing[:, 3], vel_graphing[:, 1], label='Vy')
    plt.plot(vel_graphing[:, 3], vel_graphing[:, 2], label='Vz')
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (m/s)')
    plt.title('Velocity vs Time')
    plt.legend()

    # graph position data
    plt.figure()
    plt.plot(dist_graphing[:, 3], dist_graphing[:, 0], label='Px')
    plt.plot(dist_graphing[:, 3], dist_graphing[:, 1], label='Py')
    plt.plot(dist_graphing[:, 3], dist_graphing[:, 2], label='Pz')
    plt.xlabel('Time (s)')
    plt.ylabel('Position (m)')
    plt.title('Position vs Time')
    plt.legend()
    plt.show()