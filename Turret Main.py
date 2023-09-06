
# Camera Imports
import cv2
import PiCamera

# Servo Imports
from adafruit_servokit import ServoKit as Servo
kit = Servo(channels=16) # The Adafruit Raspberry Pi hat for the Servos has 16 Pwm Channels to use.
                         # Here I am making all of the channels active

# Maths and Time Imports
import numpy as np
import os
import time
from matplotlib import pyplot as pltd

def InitialiseAndCalibrate (kit):

    # Enable Servos and Set to 0
    kit.servo[0].angle(x) # In this case x denotes any angle variable for the time being, probably 0 degrees (max 180 degrees)
                          # servo[0] denotes the PWM channel (Which Motor is turning)
    time.sleep(3) # Wait 3 seconds

    kit.servo[0].angle(y) # In this case y denotes any angle variable for the time being, probably 180 degrees

    time.sleep(3) # Wait 3 seconds 

    kit.servo[0].angle(x) # Sets angle back to original position

    # Enable camera
    cap = cv2.VideoCapture(0) #cv2 will use Camera 0 (Default camera), in this case is the Raspberry Pi camera
    cap.set(3, 640) # Setting the Height,
    cap.set(4, 420) # and Width of the capture

    return cap