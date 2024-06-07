import cv2

for index in camera_indexes:
    cap = cv2.VideoCapture(index + cv2.CAP_V4L2)
    if not cap.isOpened():
        print(f"Failed to open camera {index}")
        continue

    print(f"Trying camera {index}...")

    while True:
        success, frame = cap.read()
        if not success:
            print(f"No frame captured from camera {index}")
            break

        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        print(f"Frame captured from camera {index}")

    cap.release()
