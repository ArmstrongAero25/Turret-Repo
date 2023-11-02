import cv2
import numpy as np
from gfd.py.video.capture import VideoCaptureThreading

cv2.startWindowThread() #make the window
cap = VideoCaptureThreading(cv2.CAP_V4L2) # Start the Capture

cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv2.CAP_PROP_FPS, 24)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

cap.start()
c = cv2.waitKey(1)
while c != 27:

    ret, frame = cap.read() # Read the input video/stream
    gray = cv2.cvtColor(np.float32(frame), cv2.COLOR_BGR2GRAY) # Make the Frame gray
        
    # read haacascade to detect people in input image
    Person_cascade = cv2.CascadeClassifier("Desktop/haarcascade_upperbody.xml")
    # TODO: List the bread crumbs that lead up to the project contenents (the xml file in this case) instead of accessing the desktop.
    # For example: Say the main file was in /Python(the projects directory)/BOT(the directory in the projects directory
    # containing the files for the actual project) and it needed
    # to access a text file: you'd want to specify the bread crumbs that lead up to the contenents of the text file
    # and if it's in the same folder as the main file you should accomodate for that as well.
    # /Python/BOT/token.txt is accessed from /Python/BOT/main

    # detects people in the input image
    gray = np.array(gray, dtype = 'uint8')
    People = Person_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE) # Find People in the Image
    print('Number of detected People:', len(People))

    # loop over all the detected people
    #for (x,y,w,h) in People:
        # To draw a rectangle around the detected person  
        #cv2.rectangle(gray,(x,y),(x+w,y+h),(0,255,255),2)
        
    cv2.imshow('Output', gray) # Display the Frame

    # Stop the code when the ESC key is pressed.

cap.stop()
cap.release()
cv2.destroyAllWindows()
