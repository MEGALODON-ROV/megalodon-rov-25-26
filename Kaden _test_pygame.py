import pygame
from time import sleep
from kaden_testing import thruster_output
#import math function
#import pygame: imports the Pygame library for joystick input
#from time import sleep: allows delay in execution
#example: eating food you don't constantly eat food but one at a time

pygame.init()
#starts all Pygame modules
pygame.joystick.init()
#sets up the joystick subsystem
if pygame.joystick.get_count() == 0:
    print("No joystick detected.")
else:
    # Initialize the first joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Joystick initialized:", joystick.get_name())

    loop = True
    while loop:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          loop = False
    
        # Get joystick values
      Lx = joystick.get_axis(0)  # Left joystick X axis (left-right)
      Ly = joystick.get_axis(1)  # Left joystick Y axis (up-down)
      Rx = joystick.get_axis(2)  # Right joystick X axis (left-right)
        
      A = joystick.get_axis(3)  # Left trigger (or button)
      B = joystick.get_axis(4)  # Right trigger (or button)
    
        # Call thruster output function
      output = thruster_output(Lx, Ly, Rx, A, B)

        # Print thruster values
      print(output)

        # Add a small delay to reduce CPU usage
      sleep(0.1)

pygame.quit()