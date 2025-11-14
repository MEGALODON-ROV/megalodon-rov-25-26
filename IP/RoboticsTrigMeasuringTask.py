import math
import numpy

def tangent(angle):
    ret1 = angle / 2
    ret1 = math.radians(ret1)
    ret1 = math.tan(ret1)
    return ret1

def findSize(angle1, angle2, movement):

    #Find distance 1

    num = movement * tangent(angle2)
    denom = tangent(angle1) - tangent(angle2)
    num = num / denom
    
    #Angle conversion

    ret2 = tangent(angle1)
    ret2 *= num
    ret2 *= 2

    #Starting distance, real size
    return num, ret2


