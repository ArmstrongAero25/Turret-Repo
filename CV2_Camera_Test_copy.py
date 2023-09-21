import cv2
import numpy as np

cv2.startWindowThread() # Start the Window
cap = cv2.VideoCapture(-1, cv2.CAP_V4L2) # Start the Capture
# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read() # Read the input video
    frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA) # Resize the frame
    cv2.imshow('Input', frame) # Display the Frame
    gray = cv2.cvtColor(np.float32(frame), cv2.COLOR_BGR2GRAY) # Make the Frame gray
    
    # read haacascade to detect faces in input image
    Person_cascade = cv2.CascadeClassifier("Desktop/haarcascade_fullbody.xml")

    # detects people in the input image
    gray = np.array(gray, dtype = 'uint8')

    People = Person_cascade.detectMultiScale(gray, 1.1, 2, 0) # Find People in the Image
    print('Number of detected People:', len(People))

    # loop over all the detected people
    for (x,y,w,h) in People:

        # To draw a rectangle around the detected face  
        cv2.rectangle(gray,(x,y),(x+w,y+h),(0,255,255),2)


    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
