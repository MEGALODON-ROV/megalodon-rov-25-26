import pygame
import SalasaTest
from time import sleep

pygame.init()
pygame.joystick.init()

loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False

    #get number of joystick connected
    joystick_count = pygame.joystick.get_count()
    print(joystick_count)


    #initilize joystick
    for joy in range(joystick_count):
        joystick = pygame.joystick.Joystick(joy)
        joystick.init()
        print(f'Name: {joystick.get_name}')

        #read all axes
        message = []
        axes = joystick.get_numaxes()
        for yx in range(axes):
            axis = joystick.get_axis(yx)
            message.append(axis)
            print(f'Name: {yx} Value: {axis} ')
        #read buttons
        buttons = joystick.get_numbuttons()
        for i in range(buttons):
            butt = joystick.get_button(i)
            message.append(butt)
            print(f'number: {i} return {butt}')
        #
        Lx = message[0]
        Ly = message[1]*-1
        Rx = message[3]
        A = message[6]
        B = message[7]
        
        output = SalasaTest.joystick(Ly, Lx, Rx, A,B)
        print(output) 
pygame.quit()




       

