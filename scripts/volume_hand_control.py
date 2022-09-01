import cv2
import time
import numpy as np
import hand_tracking_module as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

w_cam, h_cam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, w_cam)
cap.set(4, h_cam)
p_time = 0
detector = htm.handDetector(detection_con=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
vol_range = volume.GetVolumeRange()
min_vol = vol_range[0]
max_vol = vol_range[1]
vol = 0
vol_bar = 400

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = detector.find_hands(frame)
    lm_list = detector.find_position(frame, draw=False)

    if len(lm_list) != 0:
        # print(lm_list[4], lm_list[8])

        x1, y1 = lm_list[4][1], lm_list[4][2]
        x2, y2 = lm_list[8][1], lm_list[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(frame, (x1, y1), 5, (255, 0, 255), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 5, (255, 0, 255), cv2.FILLED)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
        cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x1 - x2, y1 - y2)

        vol = np.interp(length, [13, 200], [min_vol, max_vol])
        vol_bar = np.interp(length, [13, 200], [400, 150])
        volume.SetMasterVolumeLevel(vol, None)
        print(int(length), vol)

        if length < 50:
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(frame, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(frame, (50, int(vol_bar)), (85, 400), (0, 255, 0), cv2.FILLED)

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
