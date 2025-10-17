import pygame
import SalasaTest
import serial
from time import sleep

pygame.init()
pygame.joystick.init()

arduino = serial.Serial("COM3", 9600)
loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False

    #get number of joystick connected
    joystick_count = pygame.joystick.get_count()
    


    #initilize joystick
    for joy in range(joystick_count):
        joystick = pygame.joystick.Joystick(joy)
        joystick.init()
       
        #read all axes
        message = []
        axes = joystick.get_numaxes()
        for yx in range(axes):
            axis = joystick.get_axis(yx)
            message.append(axis)
            
        #read buttons
        buttons = joystick.get_numbuttons()
        for i in range(buttons):
            butt = joystick.get_button(i)
            message.append(butt)
            
        #
        Lx = message[0]
        Ly = message[1]*-1
        Rx = message[3]
        A = message[6]
        B = message[7]
        
        output = SalasaTest.joystick(Lx, Ly, Rx, A, B)
        
        output = output.encode("ascii")

        arduino.write(output) 

        received = arduino.readline().decode("ascii")
        print(received)

        print(output) 
        sleep(0.5)
pygame.quit()
arduino.close()

       

