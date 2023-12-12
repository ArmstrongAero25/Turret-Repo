import cv2
from adafruit_servokit import ServoKit
import numpy as np
import time
from multiprocessing import Process, Queue
import pygame

def init_camera(width, height, fps_min, frame_queue):
    cap = cv2.VideoCapture(0 + cv2.CAP_V4L2)
    cap.set(3, width)
    cap.set(4, height)
    cap.set(cv2.CAP_PROP_FPS, fps_min)

    # Start a separate process for capturing frames
    capture_process = Process(target=capture_frames, args=(cap, frame_queue))
    capture_process.start()

    return cap, capture_process

def capture_frames(cap, queue):
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        queue.put(frame)

def control_servos(target_x, target_y, center_x, center_y, pan_servo_position, tilt_servo_position, servo_speed, kit):
    delta_x = center_x - target_x
    delta_y = center_y - target_y

    pan_servo_position += delta_x // servo_speed
    tilt_servo_position += delta_y // servo_speed

    pan_servo_position = max(0, min(180, pan_servo_position))
    tilt_servo_position = max(0, min(180, tilt_servo_position))

    kit.servo[0].angle = pan_servo_position
    kit.servo[1].angle = tilt_servo_position

def detect_objects(frame, net, confidence_threshold=0.2):
    height, width = frame.shape[:2]

    # Preprocess the image for object detection
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)

    # Set the input to the pre-trained MobileNet SSD
    net.setInput(blob)

    # Run the forward pass to get detections
    detections = net.forward()

    # Process each detection
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        # Filter out weak detections
        if confidence > confidence_threshold:
            # Extract the bounding box coordinates
            box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
            (startX, startY, endX, endY) = box.astype("int")

            return (startX, startY, endX, endY)

    return None

def play_notification_sound():
    pygame.mixer.init()
    pygame.mixer.music.load("BuildinASentry.mp3")  # Change this to the path of your notification sound file
    pygame.mixer.music.play()
    time.sleep(2)  # Adjust the sleep time based on the duration of your notification sound

def main():
    width, height = 640, 480
    fps_min, fps_max = 30, 60

    kit = ServoKit(channels=16)
    frame_queue = Queue()

    cap, capture_process = init_camera(width, height, fps_min, frame_queue)

    # Download the MobileNet SSD model
    net = cv2.dnn.readNetFromCaffe(
        'MobileNetSSD_deploy.prototxt',
        'MobileNetSSD_deploy.caffemodel'
    )

    center_x, center_y = width // 2, height // 2
    pan_servo_position, tilt_servo_position = 90, 90
    servo_speed = 10

    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()

            # Detect objects in the frame
            object_box = detect_objects(frame, net)

            if object_box is not None:
                (startX, startY, endX, endY) = object_box
                target_x, target_y = (startX + endX) // 2, (startY + endY) // 2

                control_servos(target_x, target_y, center_x, center_y, pan_servo_position, tilt_servo_position, servo_speed, kit)

                # Play notification sound
                play_notification_sound()

            cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Terminate the capture process
    capture_process.terminate()
    capture_process.join()

    # Release the camera
    cap.release()

    # Close all OpenCV windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()