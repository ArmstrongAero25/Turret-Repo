import numpy as np
import cv2
from adafruit_servokit import ServoKit


def Main():
    width, height = 640, 480
    kit = ServoKit(channels=16)
    servo_speed = 10
    
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    
    cv2.startWindowThread()
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened:
        print('--(!)Error opening video capture')
        exit(0)
        
    while (True):

        ret, frame = cap.read()
        if not ret:
            break

        elif frame is None:
            print('--(!) No captured frame -- Break!')
            break
        find_People(frame, hog, width, height, kit, servo_speed)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        cap.release()  # Release Capture
        cv2.destroyAllWindows()  # Destroy Window
        cv2.waitKey(1)


def find_People(frame, kit, servo_speed, hog, width, height):
    frame = cv2.resize(frame, (width, height))
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    
    boxes, weights = hog.detectMultiScale(gray, winStride=(8, 8))
    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
    for (xA, yA, xB, yB) in boxes:
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
        if cv2.rectangle:
            print("Detected")
            turn_servo(xA, yA, xB, yB, kit, servo_speed)
            
    return frame

def turn_servo(xA, yA, xB, yB, kit, servo_speed):
    DeltaX = xA - xB // servo_speed
    DeltaY = yA - yB // servo_speed

    pan_servo_position += DeltaX
    tilt_servo_position += DeltaY

    pan_servo_position = max(0, min(180, pan_servo_position))
    tilt_servo_position = max(0, min(180, tilt_servo_position))

    kit.servo[0].angle = pan_servo_position
    kit.servo[1].angle = tilt_servo_position


##### Main ####

if __name__ == "__Main__":
  Main()