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
    axes = joystick.get_numaxes()
    for yx in range(axes):
        axis = joystick.get_axis(yx)
        print(f'Name: {yx} Value: {axis} ')

    buttons = joystick.get_numbuttons()
    for i in range(buttons):
        butt = joystick.get_button(i)
        print(f'number: {i} return {butt}')




       

