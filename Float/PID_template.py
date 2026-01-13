kP = 0
kI = 0
kD = 0
kP_HOLD = 0
kD_HOLD = 0

def PID(target_position):
    current_position = 0 # REPLACE with sensor returned value
    error = current_position - target_position
    integral = 0
    previous_error = 0
    derivative = 0
    ERROR_ALLOWED = 20 # cm
    TIME_TO_HOLD = 40 # seconds
    time_started = 0 # REPLACE with current time function
    # printf ("Target position: %f\n", target_position)

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
    
    # some kind of code to hold position?
    # either more PID-based or if robot is nice there could be some
        # throttle value that just keeps it in place
    while (0 - time_started < TIME_TO_HOLD):    # REPLACE 0 WITH CURRENT TIME FUNCTION
        # maintain position
        # USE THE OUTPUT VALUE
        pass