import lauraTest
import pygame
from time import sleep

pygame.init()       # Initialize Pygame modules
pygame.joystick.init()  # Initialize joystick module, sets up joystick subsystem

# main loop
loop = True
while loop:
    message = []        # new message list for each loop iteration

    for event in pygame.event.get():        # pygame.event.get() returns a list
                                            # of all events (quit, button pressed, etc)
        # stop looping if window is closed
        if event.type == pygame.QUIT:       # an event triggered when user closes window
            loop = False
        
    # detect number of JOYSTICKS connected
    joystickNum = pygame.joystick.get_count()
    print(joystickNum)

    # loop through every joystick
    for i in range(joystickNum):
        joystick = pygame.joystick.Joystick(i)  # create Joystick object
        joystick.init()  # initialize the joystick object so we can read its values
        print("Joystick name {}: {}".format(i, joystick.get_name()))

        # get AXIS values for joystick
        axes = joystick.get_numaxes()       # returns number of axes on joystick variable with each
                                            # with each axis corresponding to a stick or trigger
        for i in range(axes):       # print axis values
            message.append(joystick.get_axis(i))
            print("Axis {} value: {}".format(i, joystick.get_axis(i)))

        # get BUTTON values for joystick
        buttons = joystick.get_numbuttons()
        for i in range(buttons):    # print button values
            message.append(joystick.get_button(i))
            print("Button {} value: {}".format(i, joystick.get_button(i)))

    # gotten from prev year's code
    Lx = message[0]
    Ly = message[1]
    Rx = message[3]
    A = message[5]  # orange button
    B = message[6]  # button behind orange button

    # convert to arduino format to prepare to send
    messageToSend = lauraTest.convertForArduino(Ly, 1, Lx, 1, Rx, A, B)
    messageToSend = messageToSend.encode("ascii")
    print("message to send: {}".format(messageToSend))

    print("type of joystick variable: {}".format(type(joystick)))

    sleep(0.1)  # add delay to avoid spamming output

pygame.quit()  # stops pygame cleanly