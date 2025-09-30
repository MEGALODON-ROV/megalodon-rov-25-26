
def joystick_value(X):
    # deadband no twich
    if X < 0.1 and X > -0.1:
        return 0
    return (X * 400)

def limit_wpm(thrusters):
    # rounding have cap
    if thrusters > 1900:
        return 1900
    elif thrusters < 1100:
        return 1100
    return int(thrusters)
# thruster values
horizontal_thrusters = [1500, 1500, 1500, 1500]
vertical_thrusters = [1500, 1500, 1500, 1500]
# thruster[0] = front left
# thruster[1] = front right
# thruster[2] = back right
# thruster[3] = back left
def joystick(Ly, Lx, Rx, A,B):
    Ly = joystick_value(Ly)
    Lx = joystick_value(Lx)
    Rx = joystick_value(Rx)
    #scaling percentage
    percent_horiz = 0.9
    percent_vert = 0.5

    Ly = joystick_value(Ly) * percent_horiz
    Lx = joystick_value(Lx) * percent_horiz
    Rx = joystick_value(Rx) * percent_horiz

    
    # base pwm values
    fl = 1500
    fr = 1500
    bl = 1500
    br = 1500

    # fr = 1500 -> Ly = 1 -> fr = 1900
    # Ly = -1 -> fr = 1100
    #forward backward
    fr += Ly 
    fl += Ly
    br += Ly
    bl += Ly
    # side to side
    fr -= Lx
    fl += Lx
    br += Lx
    bl -= Lx
    # rotate
    fr += Rx
    fl -= Rx
    br += Rx
    bl -= Rx
    #vertical 
    idk = 0
    if A == 1:
        idk = 400
    elif B == 1:
        idk = -400
    vertical1 = 1500 + idk * percent_vert
    vertical2 = 1500 + idk * percent_vert
    vertical3 = 1500 + idk * percent_vert
    vertical4 = 1500 + idk * percent_vert
    # limit wpm
    fl = limit_wpm(fl)
    fr = limit_wpm(fr)
    bl = limit_wpm(bl)
    br = limit_wpm(br)

    vertical1 = limit_wpm(vertical1)
    vertical2 = limit_wpm(vertical2)
    vertical3 = limit_wpm(vertical3)
    vertical4 = limit_wpm(vertical4)

    return str(fl) + ",", str(fr) + "/", str(bl) + ":", str(br) + "#", str(vertical1) + "*", str(vertical2) + "!", str(vertical3) + "-", str(vertical4) + "/"

