import cv2
import time
import numpy as np
import hand_tracking_module as htm

w_cam, h_cam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, w_cam)
cap.set(4, h_cam)
p_time = 0
detector = htm.handDetector(detection_con=0.7)

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = detector.find_hands(frame)

    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time

    cv2.putText(
        frame,
        f"FPS: {int(fps)}",
        (40, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3,
    )

    cv2.imshow("frame", frame)
    cv2.waitKey(1)
