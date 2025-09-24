
def joystick_value(X):
    if X < 0.1 and X > -0.1:
        return 0
    return (X * 400)



horizontal_thrusters = list()
horizontal_thrusters[1500, 1500, 1500, 1500]
vertical_thrusters = 1500
# thruster[0] = front left
# thruster[1] = front right
# thruster[2] = back right
# thruster[3] = back left
def joystick(Ly, Lx, Rx, A,B):
    Ly = joystick_value(Ly)
    Lx = joystick_value(Lx)
    Rx = joystick_value(Rx)
    A = joystick_value(A)
    B = joystick_value(B)
    if A == 1:
        vertical_thrusters += A
    elif B == 1:
        vertical_thrusters -= B

    fl = 1500
    fr = 1500
    bl = 1500
    br = 1500

    # fr = 1500 -> Ly = 1 -> fr = 1900
    # Ly = -1 -> fr = 1100

    fr += Ly 
    fl += Ly
    br += Ly
    bl += Ly

    fr -= Lx
    fl += Lx
    br += Lx
    bl -= Lx

    fr += Rx
    fl -= Rx
    br += Rx
    bl -= Rx

def round(thrusters):
    if thrusters > 1900:
        return 1900
    elif thrusters < 1100:
        return 1100
    return int(thrusters)

