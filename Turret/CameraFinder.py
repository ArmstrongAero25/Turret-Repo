import cv2

for i in range(20):
    cap = cv2.VideoCapture(i + cv2.CAP_V4L2)
    if not cap.isOpened():
        print(f"Failed to open camera {i}")
        continue

    print(f"Trying camera {i}...")

    while True:
        success, frame = cap.read()
        if not success:
            print(f"No frame captured from camera {i}")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        print(f"Frame captured from camera {i}")

    cap.release()
