from adafruit_servokit import ServoKit
from picamera2 import Picamera2
import Turret_Exceptions as TE
import numpy as np
import vlc  # NOTE: pip install python-vlc
import cv2


### Constant Values ###
servo_speed = 10
kit = ServoKit(channels=16)


def main():
    # This is the program entry point.
    print("--(note) Initialising..")

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # cv2.startWindowThread() HEXA-SOFTWARE-DEV: Turns out
    # the Headless version of OpenCV python doesn't require this,
    # so I'm temporarily removing all things to do with window display.

    picam2 = Picamera2()
    picam2.start()

    # media = vlc.MediaPlayer("Sounds/BuildinASentry.mp3")
    # If the rpi doesn't have a bulit in speaker this may not work.
    # media.play()

    print("--(note) Initialisation successful.")

    while True:
        frame = picam2.capture_array()
        # Success contains a value to convey if the data was returned successfully.

        print("Capture Success!")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        find_people(gray, hog)


def find_people(gray, hog):
    # This will find a target within a given frame.
    boxes, _ = hog.detectMultiScale(gray, winStride=(8, 8))
    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    for (xA, yA, xB, yB) in boxes:
        turn_servo(xA, yA, xB, yB)


def turn_servo(xA, yA, xB, yB):
    # This will turn the servo by the given coordinates.
    # Calm: Hey, as long as this works, grand.
    pan_servo_position = (xA + xB) // servo_speed
    tilt_servo_position = (yA + yB) // servo_speed

    kit.servo[0].angle = max(0, min(180, pan_servo_position))
    kit.servo[1].angle = max(0, min(180, tilt_servo_position))

    # Calm1403: Here I like to visualise one of those navy turrets they have on warships turning up and down.
    # It's a nice visualisation.


if __name__ == "__main__":
    main()
