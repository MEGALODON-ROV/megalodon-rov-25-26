pidLateral = [0, 0, 0]
pidAngular = [0, 0, 0]
pidUp = [0, 0, 0]
pidDown = [0, 0, 0]

maintainPos = True

def PID(x, y, z, pitch, roll, yaw):
    kP = 0
    kI = 0
    kD = 0
    current_position = 0 # REPLACE with sensor returned value
    lateralError = [current_position - x, current_position - y, current_position - z]
    angularError = [current_position - pitch, current_position - roll, current_position - yaw]
    integral = 0
    previous_error = 0
    derivative = 0
    # printf ("Target position: %f\n", target_position)
    while maintainPos:
        # when going down
        if target_position <= current_position:
            kP = pidDown[0]
            kI = pidDown[1]
            kD = pidDown[2]
        
        # when going up
        else:
            kP = pidUp[0]
            kI = pidUp[1]
            kD = pidUp[2]
        
        current_position = 0 # REPLACE with sensor returned value
        error = current_position - target_position
        integral += error
        derivative = error - previous_error
        output = kP * error + kI * integral + kD * derivative

        previous_error = error

        # USE THE OUTPUT VALUE
        # DELAY TO PREVENT THE LOOP FROM RUNNING TOO FAST
    '''
    # loop to get to target position
    while (abs(error) > ERROR_ALLOWED):  # Continue until the error is within a small range
        current_position = 0 # REPLACE with sensor returned value
        error = current_position - target_position
        integral += error
        derivative = error - previous_error
        output = kP * error + kI * integral + kD * derivative
        if output < 1100:
            output = 1100  # Minimum throttle value
        elif output > 1900:
            output = 1900  # Maximum throttle value
        
        # USE THE OUTPUT VALUE
        
        previous_error = error
        # Add delay to prevent the loop from running too fast
    '''
    '''
    # some kind of code to hold position?
    # either more PID-based or if robot is nice there could be some
        # throttle value that just keeps it in place
    while (0 - time_started < TIME_TO_HOLD):    # REPLACE 0 WITH CURRENT TIME FUNCTION
        # maintain position
        # USE THE OUTPUT VALUE
        pass
    '''