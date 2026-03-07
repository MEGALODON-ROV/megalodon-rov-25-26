import accelerometer
import time

pidLateral = [0, 0, 0]
pidAngular = [0, 0, 0]
pidUp = [0, 0, 0]
pidDown = [0, 0, 0]
output = [0, 0, 0, 0, 0, 0]      # CHANGE to be a list in format of thruster values
maintainPos = True

def depthPID(goalZ):
    kP = 0
    kI = 0
    kD = 0
    currZ = accelerometer.position[2]
    error = goalZ - currZ
    integral = 0
    previous_error = 0
    derivative = 0
    # printf ("Target position: %f\n", target_position)
    while maintainPos:
        if goalZ <= currZ:
            kP = pidDown[0]
            kI = pidDown[1]
            kD = pidDown[2]
        
        else:
            kP = pidUp[0]
            kI = pidUp[1]
            kD = pidUp[2]
        
        currZ = accelerometer.position[2]
        error = goalZ - currZ
        integral += error
        derivative = error - previous_error

        # CHANGE make sure output index is correct for depth thrusters
            # and values are bounded correctly for thrusters
        output[0] = kP * error + kI * integral + kD * derivative

        previous_error = error

        # USE THE OUTPUT VALUE (send to thrusters)
        # DELAY TO PREVENT THE LOOP FROM RUNNING TOO FAST
        time.sleep(0.3)

def lateralPID(x, y):
    kP = pidLateral[0]
    kI = pidLateral[1]
    kD = pidLateral[2]

    currX = accelerometer.position[0]
    errorX = x - currX
    integralX = 0
    prevErrX = 0
    derivativeX = 0

    currY = accelerometer.position[1]
    errorY = y - currY
    integralY = 0
    prevErrY = 0
    derivativeY = 0
    # printf ("Target position: %f\n", target_position)
    while maintainPos:
        # handle x first
        currX = accelerometer.position[0]
        errorX = x - currX
        integralX += errorX
        derivativeX = errorX - prevErrX

        # CHANGE make sure output index is correct for lateral thrusters
            # and values are bounded correctly for thrusters
        output[0] = kP * errorX + kI * integralX + kD * derivativeX

        prevErrX = errorX

        # handle y next
        currY = accelerometer.position[1]
        errorY = y - currY
        integralY += errorY
        derivativeY = errorY - prevErrY

        # CHANGE make sure output index is correct for lateral thrusters
            # and values are bounded correctly for thrusters
        output[0] = kP * errorY + kI * integralY + kD * derivativeY
        prevErrY = errorY
        # DELAY TO PREVENT THE LOOP FROM RUNNING TOO FAST
        time.sleep(0.3)

def angularPID(pitch, roll, yaw):
    kP = pidAngular[0]
    kI = pidAngular[1]
    kD = pidAngular[2]
    currAngles = [0, 0, 0] # REPLACE with sensor returned value
    errors = [pitch - currAngles[0], roll - currAngles[1], yaw - currAngles[2]]
    integral = 0
    previous_error = 0
    derivative = 0
    # printf ("Target position: %f\n", target_position)
    while maintainPos:
        current_position = 0 # REPLACE with sensor returned value
        error = current_position - pitch
        integral += error
        derivative = error - previous_error
        output = kP * error + kI * integral + kD * derivative

        previous_error = error

        # USE THE OUTPUT VALUE
        # DELAY TO PREVENT THE LOOP FROM RUNNING TOO FAST
        time.sleep(0.3)