# movement map
# (front left, front right, back left, back right)
# Lx = side to side, right = positive (1900, 1100, 1100, 1900)
# Ly = forward/back, forward = positive (1900, 1900, 1900, 1900)
# Rx → rotation of joystick (left = positive direction, right = negative direction)
        # ()
# A / B → buttons for up /down respectively (1 = full power, 0 = no power)

frontLeftThruster = 1500
frontRightThruster = 1500
backLeftThruster = 1500
backRightThruster = 1500
verticalThruster = 1500

def lateralScale(Lx):
    return Lx * 400

def forwardBackwardScale(Ly):
    return Ly * 400

def rotationScale(Rx):
    return Rx * 400

def moveForwardBackwards(Ly):
    fwdPower = forwardBackwardScale(Ly)
    frontLeftThruster = fwdPower + 1500
    frontRightThruster = fwdPower + 1500
    backLeftThruster = fwdPower + 1500
    backRightThruster = fwdPower + 1500
    return (frontLeftThruster, frontRightThruster, backLeftThruster, backRightThruster)

def crabbing(Lx):
    crabPower = lateralScale(Lx)
    frontLeftThruster = crabPower + 1500
    frontRightThruster = -crabPower + 1500
    backLeftThruster = -crabPower + 1500
    backRightThruster = crabPower + 1500
    return (frontLeftThruster, frontRightThruster, backLeftThruster, backRightThruster)

def rotate(Rx):
    rotatePower = rotationScale(Rx)
    frontLeftThruster = -rotatePower + 1500
    frontRightThruster = -(frontLeftThruster)
    backLeftThruster = -rotatePower + 1500
    backRightThruster = -(backLeftThruster)
    return (frontLeftThruster, frontRightThruster, backLeftThruster, backRightThruster)

def verticalMovement(A, B):
    if (A == 1):
        verticalThruster = 1900
    elif (B == 1):
        verticalThruster = 1100
    else:
        verticalThruster = 1500

    return verticalThruster
