import cv2
import numpy as np
from gfd.py.video.capture import VideoCaptureThreading

cv2.startWindowThread() #make the window
cap = VideoCaptureThreading(-1, cv2.CAP_V4L2) # Start the Capture

cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

cap.set(cv2.CAP_PROP_FPS, 28)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

cap.start()
while True:

    ret, frame = cap.read() # Read the input video

    frame = cv2.resize(frame, None, fx=0.6, fy=0.5, interpolation=cv2.INTER_AREA) # Resize the frame

    cv2.imshow('Output', frame) # Display the Frame
    gray = cv2.cvtColor(np.float32(frame), cv2.COLOR_BGR2GRAY) # Make the Frame gray
        
    # read haacascade to detect people in input image
    Person_cascade = cv2.CascadeClassifier("Desktop/haarcascade_upperbody.xml")

    # detects people in the input image
    gray = np.array(gray, dtype = 'uint8')
    People = Person_cascade.detectMultiScale(gray, 1.05, 1, 0) # Find People in the Image
    print('Number of detected People:', len(People))

    # loop over all the detected people
    for (x,y,w,h) in People:
        # To draw a rectangle around the detected person  
        cv2.rectangle(gray,(x,y),(x+w,y+h),(0,255,255),2)

    c = cv2.waitKey(1)
    if c == 27:
        break
cap.stop()

cv2.destroyAllWindows()
