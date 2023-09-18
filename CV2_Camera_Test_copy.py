import cv2


cv2.startWindowThread()
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input', frame)

    grey = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)

    # read haacascade to detect faces in input image
    Person_cascade = cv2.CascadeClassifier('haarcascades\haarcascade_fullbody.xml')

    # detects faces in the input image
    People = Person_cascade.detectMultiScale(gray, 1.1, 2)
    print('Number of detected People:', len(People))

    # loop over all the detected faces
    for (x,y,w,h) in People:

        # To draw a rectangle around the detected face  
        cv2.rectangle(cap,(x,y),(x+w,y+h),(0,255,255),2)


    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
