import pygame
import serial
from time import sleep


arduino = serial.Serial('COM4', 9600)
sleep(3)
loop = True

pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock()
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Quit")
            loop = False

    arduino.write("Hello World".encode()) 

    received = arduino.readline().decode()
    print(received)

    sleep(0.03)