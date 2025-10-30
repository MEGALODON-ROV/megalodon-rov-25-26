import pygame
from time import sleep
import serial

pygame.init()
pygame.joystick.init()

#joystick = pygame.joystick.Joystick(0)
#joystick.init()

loop = True

def clamp(value, minVal, maxVal):
    newVal = max(min(maxVal, value), minVal)
    return newVal

def thrusterMap(Lx: int, Ly: int, Rx: int, A: int, B: int, xPercent: int, yPercent: int):
	
    if Lx < -0.1:
        StickX = (Lx * 1.1 * xPercent) + 0.1
    elif Lx > 0.1:
        StickX = (Lx * 1.1 * xPercent) - 0.1
    else:
        StickX = 0

    if Ly < -0.1:
        StickY = (Ly * 1.1 * yPercent) + 0.1
    elif Ly > 0.1:
        StickY = (Ly * 1.1 * yPercent) - 0.1
    else:
        StickY = 0

    if Rx < -0.2:
        Rotation = (Rx * 1.2) + 0.2
    elif Rx > 0.2:
        Rotation = (Rx * 1.2) - 0.2
    else:
        Rotation = 0

    fl = (clamp(StickX + StickY, -1, 1) * 400) + 1500
    fr = (clamp(-StickX + StickY, -1, 1) * 400) + 1500
    bl = (clamp(-StickX + StickY, -1, 1) * 400) + 1500
    br = (clamp(StickX + StickY, -1, 1) * 400) + 1500

    fl = round(clamp(fl - (Rotation * 200), 1100, 1900))
    fr = round(clamp(fr + (Rotation * 200), 1100, 1900))
    bl = round(clamp(bl - (Rotation * 200), 1100, 1900))
    br = round(clamp(br + (Rotation * 200), 1100, 1900))

    if A > 0.5 and B < 0.5:
        flV = 1900
        frV = 1900
        blV = 1900
        brV = 1900
    elif B > 0.5 and A < 0.5:
        flV = 1100
        frV = 1100
        blV = 1100
        brV = 1100
    else:
        flV = 1500
        frV = 1500
        blV = 1500
        brV = 1500

    output = str(fl) + "+" + str(fr) + "-" + str(bl) + "*" + str(br) + "/" + str(flV) + "(" + str(frV) + ")" + str(blV) + "[" + str(brV)
    
    #fl, fr, bl, br, flV, frV, blV, brV
    
    return output
#X - right, Y - forward 

timer = 0

while loop and timer < 200:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False

    joystickX = 0.5#joystick.get_axis(2)
    joystickY = 1#-joystick.get_axis(3)
    joystickR = 0#-joystick.get_axis(0)
    joystickA = 0#clamp(-joystick.get_axis(1), 0, 1)
    joystickB = 0#clamp(joystick.get_axis(1), 0, 1)
    print(thrusterMap(joystickX, joystickY, joystickR, joystickA, joystickB, 1, 1))
    timer += 1
    message = thrusterMap(joystickX, joystickY, joystickR, joystickA, joystickB, 1, 1).encode("ascii")
    arduino.write(message)

    print(arduino)
    sleep(0.1)

print("end")

pygame.quit()