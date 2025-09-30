import cv2
import mediapipe as mp
import numpy as np
import pyautogui
from math import hypot
import time

# -----------------------------
# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)  # track 1 hand
mp_draw = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)

# Get screen size
screen_width, screen_height = pyautogui.size()

# Previous cursor point for smoothing
prev_x, prev_y = 0, 0
smooth_factor = 5

# Click cooldown timers
last_left_click = 0
last_right_click = 0
click_cooldown = 0.5  # seconds

# -----------------------------
while True:
    success, img = cap.read()
    if not success:
        continue

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get finger tips
            thumb_x = int(hand_landmarks.landmark[4].x * img.shape[1])
            thumb_y = int(hand_landmarks.landmark[4].y * img.shape[0])
            index_x = int(hand_landmarks.landmark[8].x * img.shape[1])
            index_y = int(hand_landmarks.landmark[8].y * img.shape[0])
            middle_x = int(hand_landmarks.landmark[12].x * img.shape[1])
            middle_y = int(hand_landmarks.landmark[12].y * img.shape[0])
            pinky_x = int(hand_landmarks.landmark[20].x * img.shape[1])
            pinky_y = int(hand_landmarks.landmark[20].y * img.shape[0])

            # -----------------------------
            # Volume control (thumb + index pinch)
            distance_thumb_index = hypot(index_x - thumb_x, index_y - thumb_y)
            if distance_thumb_index < 40:  # pinch detected
                pyautogui.press("volumedown")
                cv2.putText(img, "Volume Down", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            elif distance_thumb_index > 150:
                pyautogui.press("volumeup")
                cv2.putText(img, "Volume Up", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            # -----------------------------
            # Cursor movement with index finger
            cursor_x = np.interp(index_x, [0, img.shape[1]], [0, screen_width])
            cursor_y = np.interp(index_y, [0, img.shape[0]], [0, screen_height])

            smooth_x = prev_x + (cursor_x - prev_x) / smooth_factor
            smooth_y = prev_y + (cursor_y - prev_y) / smooth_factor
            pyautogui.moveTo(smooth_x, smooth_y)
            prev_x, prev_y = smooth_x, smooth_y

            # -----------------------------
            # Left Click (index + middle pinch)
            distance_index_middle = hypot(index_x - middle_x, index_y - middle_y)
            if distance_index_middle < 30 and time.time() - last_left_click > click_cooldown:
                pyautogui.click(button='left')
                last_left_click = time.time()
                cv2.putText(img, "Left Click", (50,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

            # Right Click (thumb + pinky pinch)
            distance_thumb_pinky = hypot(thumb_x - pinky_x, thumb_y - pinky_y)
            if distance_thumb_pinky < 30 and time.time() - last_right_click > click_cooldown:
                pyautogui.click(button='right')
                last_right_click = time.time()
                cv2.putText(img, "Right Click", (50,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    # Show webcam feed
    cv2.imshow("Hand Tracking - Cursor, Volume & Click", img)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
