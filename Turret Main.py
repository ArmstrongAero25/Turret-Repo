
# Camera Imports
import cv2
#import Picamera

# Servo Imports
from adafruit_servokit import ServoKit as Servo


# Maths and Time Imports
import numpy as np
import os
import time
#]from matplotlib import pyplot as pltd

kit = Servo(channels = 16) # The Adafruit Raspberry Pi hat for the Servos has 16 Pwm Channels to use.
                           # Here I am making all of the channels active


def InitialiseAndCalibrate (kit):
    
    print (type(kit))
    
    # Enable Servos and Set to 0
    kit.servo[0].angle = 0 # In this case x denotes any angle variable for the time being, probably 0 degrees (max 180 degrees)
                          # servo[0] denotes the PWM channel (Which Motor is turning)
    time.sleep(3) # Wait 3 seconds

    kit.servo[0].angle = 180 # In this case y denotes any angle variable for the time being, probably 180 degrees

    time.sleep(3) # Wait 3 seconds 

    kit.servo[0].angle = 0 # Sets angle back to original position


# This Will go in Process 1
def LookforPeople():
    # Person/Object Id code
  
    # Enable camera
    cv2.startWindowThread()
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2) #cv2 will use Camera 0 (Default camera), in this case is the Raspberry Pi camera

    #while (True):
        
        #Set Capture Frame
        frame = cap.read()
        
        #Display the frame
        cv2.imshow('frame', frame)
        
        cap.set(3, 640) # Setting the Height,
        cap.set(4, 420) # and Width of the capture

# The rest of the code will come under this. So when a Person is Found, the Variable will become true and
# a signal will be sent to the Servo Function to turn the servos to the X and Y coordinates of the person in the frame.
      
    return cap, Personfound # Filler Variable to signify that a person is found on the feed


#This Will go In Process 2
def SearchPattern(PersonFound): # This func. will turn the Panning Servo back and forth to cover
                     # a wider search fov while the camera is looking for people
    while PersonFound != True:
        kit.servo(0).throttle = 0.5 

        time.sleep (3)

        kit.servo(0).throttle = -0.5

        
###################Main############################
    
InitialiseAndCalibrate (kit)
cap, Personfound = LookforPeople ()

