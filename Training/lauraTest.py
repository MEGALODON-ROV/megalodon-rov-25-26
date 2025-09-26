# movement map
# (front left, front right, back left, back right)
# Lx = side to side, right = positive (1900, 1100, 1100, 1900)
# Ly = forward/back, forward = positive (1900, 1900, 1900, 1900)
# Rx --> rotation of joystick, left = positive
        # (1100, 1900, 1100, 1900) --> if drawing the vectors, it is a diamond shape
# A / B --> buttons for up /down respectively (only full power up/down or no movement --> binary)

thrusters = {
    "frontLeft": 1500,
    "frontRight": 1500,
    "backLeft": 1500,
    "backRight": 1500,
    "vertical": 1500
}

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

def moveForwardBackwards(Ly, percentVert = 1):
    fwdPower = scaleInput(Ly) * percentVert     # percentVert to change how
                                                # effective moving joystick is
    for i in thrusters:
        thrusters[i] = roundThrusterValue(fwdPower + 1500)
    return (thrusters["frontLeft"], thrusters["frontRight"], 
            thrusters["backLeft"], thrusters["backRight"])

def crabbing(Lx, percentHoriz = 1):
    crabPower = scaleInput(Lx) * percentHoriz   # percentHoriz to change how
                                                # effective moving joystick is
    thrusters["frontLeft"] = roundThrusterValue(crabPower + 1500)
    thrusters["frontRight"] = roundThrusterValue(-crabPower + 1500)
    thrusters["backLeft"] = thrusters["frontRight"]
    thrusters["backRight"] = thrusters["frontLeft"]
    return (thrusters["frontLeft"], thrusters["frontRight"], 
            thrusters["backLeft"], thrusters["backRight"])

def rotate(Rx):
    rotatePower = scaleInput(Rx)

    thrusters["frontLeft"] = roundThrusterValue(-rotatePower + 1500)
    thrusters["frontRight"] = roundThrusterValue(rotatePower + 1500)
    thrusters["backLeft"] = thrusters["frontLeft"]
    thrusters["backRight"] = thrusters["frontRight"]
    return (thrusters["frontLeft"], thrusters["frontRight"], 
            thrusters["backLeft"], thrusters["backRight"])

def verticalMovement(A, B):
    if (A == 1):
        thrusters["vertical"] = 1900
    elif (B == 1):
        thrusters["vertical"] = 1100
    else:
        thrusters["vertical"] = 1500

    return thrusters["vertical"]

def convertForArduino(Ly = 0, percentVert = 1, Lx = 0, percentHoriz = 1, Rx = 0, A = 0, B = 0):
    moveForwardBackwards(Ly, percentVert)
    crabbing(Lx, percentHoriz)
    rotate(Rx)
    verticalMovement(A, B)

    # format for arduino
    parts = [
        str(thrusters["frontLeft"]),  "+",
        str(thrusters["frontRight"]), "-",
        str(thrusters["backLeft"]),   "=",
        str(thrusters["backRight"]),  "/",
        str(thrusters["vertical"]),   ")",      # there are 4 vertical thrusters
        str(thrusters["vertical"]),   "(",      # but they are all have the same output
        str(thrusters["vertical"]),   "!",
        str(thrusters["vertical"])
    ]
    return "".join(parts)