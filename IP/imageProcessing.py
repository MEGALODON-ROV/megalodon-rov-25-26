import accelerometer
import ROV_PID
import threading
import time
from enum import Enum

class primaryAxisOfMovement(Enum):
    X = 0
    Y = 1
    Z = 2

accelerometer.calibrate()

# start sensor reading in background thread so it doesn't block the PID loop
sensorThread = threading.Thread(target=accelerometer.trackPosition, daemon=True)
sensorThread.start()

# axis we will move on?
primaryAxis = primaryAxisOfMovement.Y # REPLACE with correct axis via user input???

# TAKE FIRST SNAPSHOT OF SITUATION HERE


# adjust for second snapshot
ROV_PID.maintainPos = True  # keep PID loops running
if primaryAxis == primaryAxisOfMovement.X:
    ROV_PID.lateralPID(accelerometer.position[0], 0)
    ROV_PID.depthPID(0)
elif primaryAxis == primaryAxisOfMovement.Y:
    ROV_PID.lateralPID(0, accelerometer.position[1])
    ROV_PID.depthPID(0)
elif primaryAxis == primaryAxisOfMovement.Z:
    ROV_PID.depthPID(accelerometer.position[2])
    ROV_PID.lateralPID(0, 0)
ROV_PID.angularPID(0, 0, 0)


# TAKE SECOND SNAPSHOT OF SITUATION HERE

ROV_PID.maintainPos = False  # stop PID loops once done taking snapshot