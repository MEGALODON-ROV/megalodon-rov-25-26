# movement map
# (front left, front right, back left, back right)
# Lx = side to side, right = positive (1900, 1100, 1100, 1900)
# Ly = forward/back, forward = positive (1900, 1900, 1900, 1900)
# Rx → rotation of joystick (left = positive direction, right = negative direction)
        # (1100, 1900, 1100, 1900) --> if drawing the vectors, it is a diamond shape
# A / B → buttons for up /down respectively (1 = full power, 0 = no power)

frontLeftThruster = 1500
frontRightThruster = 1500
backLeftThruster = 1500
backRightThruster = 1500
verticalThruster = 1500

def scaleInput(joystickInput):
    if joystickInput < 0.1 and joystickInput > -0.1:
        return 0    # deadzone
    return joystickInput * 400

def roundThrusterValue(thrusterValue):
    if thrusterValue > 1900:
        return 1900
    elif thrusterValue < 1100:
        return 1100
    return int(thrusterValue)

def moveForwardBackwards(Ly, percentVert):
    fwdPower = scaleInput(Ly) * percentVert     # scale to change how effective moving joystick is
    frontLeftThruster = roundThrusterValue(fwdPower + 1500)
    frontRightThruster = roundThrusterValue(fwdPower + 1500)
    backLeftThruster = roundThrusterValue(fwdPower + 1500)
    backRightThruster = roundThrusterValue(fwdPower + 1500)
    return (frontLeftThruster, frontRightThruster, backLeftThruster, backRightThruster)

def crabbing(Lx, percentHoriz):
    crabPower = scaleInput(Lx) * percentHoriz
    frontLeftThruster = roundThrusterValue(crabPower + 1500)
    frontRightThruster = roundThrusterValue(-crabPower + 1500)
    backLeftThruster = roundThrusterValue(-crabPower + 1500)
    backRightThruster = roundThrusterValue(crabPower + 1500)
    return (frontLeftThruster, frontRightThruster, backLeftThruster, backRightThruster)

def rotate(Rx):
    rotatePower = scaleInput(Rx)
    frontLeftThruster = roundThrusterValue(-rotatePower + 1500)
    frontRightThruster = roundThrusterValue(frontLeftThruster)
    backLeftThruster = roundThrusterValue(-rotatePower + 1500)
    backRightThruster = roundThrusterValue(backLeftThruster)
    return (frontLeftThruster, frontRightThruster, backLeftThruster, backRightThruster)

def verticalMovement(A, B):
    if (A == 1):
        verticalThruster = 1900
    elif (B == 1):
        verticalThruster = 1100
    else:
        verticalThruster = 1500

    return verticalThruster

def convertForArduino():
    parts = [
        str(frontLeftThruster),  "+",
        str(frontRightThruster), "-",
        str(backLeftThruster),   "=",
        str(backRightThruster),  "/",
        str(verticalThruster),   ")",
        str(verticalThruster),   "(",
        str(verticalThruster),   "!",
        str(verticalThruster)
    ]
    return "".join(parts)