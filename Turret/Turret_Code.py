import numpy as np
import vlc  # NOTE: pip install python-vlc
import cv2
from adafruit_servokit import ServoKit


def main():
    # This is the program entry point.
    print("--(note) Initialising..")
    width, height = 640, 480
    kit = ServoKit(channels=16)
    servo_speed = 10

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # cv2.startWindowThread() HEXA-SOFTWARE-DEV: Turns out
    # the Headless version of OpenCV python doesn't require this,
    # so I'm temporarily removing all things to do with window display.
    cap = cv2.VideoCapture(0 + cv2.CAP_V4L2)

    if not cap.isOpened():
        print("--(!) Error opening video capture.")
        exit(0)

    media = vlc.MediaPlayer("Sounds/BuildinASentry.mp3")
    # If the rpi doesn't have a bulit in speaker this may not work.
    media.play()

    print("--(note) Initialisation successful.")

    while True:

        success, frame = cap.read()
        # Success contains a value to convey if the data was returned successfully.

        if not (success):
            # This is essentually the same except it's a little more readable.
            # Original line: if success is None:
            print('--(!) No captured frame -- Break!')
            break

        frame = find_People(frame, hog, width, height, kit, servo_speed)

        # cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Calm1403: This is a guess but..
            # 0xFF -> 255, 255 -> 11111111 .: condition = ans(cv2.waitkey(1)) & 11111111 == (1000111?)
            # & => "Sets each bit to 1 if both bits are 1"
            # This is some crazy arithmetic.. all done in a milisecond too, this method is impresive.
            break

    cap.release()
    # cv2.destroyAllWindows()
    # cv2.waitKey(1)


def find_People(frame, hog, width, height, kit, servo_speed):
    # This will find a target within a given frame.

    frame = cv2.resize(frame, (width, height))
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    boxes, _ = hog.detectMultiScale(gray, winStride=(8, 8))
    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    for (xA, yA, xB, yB) in boxes:

        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
        print("--(note) Person detected -- Turning servo.")
        turn_servo(xA, yA, xB, yB, kit, servo_speed)

    return frame


def turn_servo(xA, yA, xB, yB, kit, servo_speed):
    # This will turn the servo by the given coordinates.

    pan_servo_position = 0
    tilt_servo_position = 0

    DeltaX = (xA + xB) // servo_speed
    DeltaY = (yA + yB) // servo_speed

    pan_servo_position = DeltaX
    tilt_servo_position = DeltaY

    pan_servo_position = max(0, min(180, pan_servo_position))
    tilt_servo_position = max(0, min(180, tilt_servo_position))

    kit.servo[0].angle = pan_servo_position
    kit.servo[1].angle = tilt_servo_position

    # Calm1403: Here I like to visualise one of those navy turrets they have on warships turning up and down.
    # It's a nice visualisation.


if __name__ == "__main__":
    main()
