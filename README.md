# Hand-Gesture
This project uses computer vision with OpenCV and MediaPipe to track hand movements in real time via a laptop camera. It detects hand landmarks (fingers, joints, palm) and enables gesture-based interactions like controlling the mouse cursor or adjusting volume with pinching/stretching.



🖱️ Mouse Cursor Control – Move the index finger in front of the webcam, and the system moves the mouse cursor accordingly.

🔊 Volume Control – Use a pinch gesture (thumb + index finger):

Bring fingers closer → Volume goes down.

Stretch fingers apart → Volume goes up.

✋ Click Gestures : 
The program calculates the distance between your index finger tip and middle finger tip.

If your index and middle fingers come very close together (less than 30 pixels in the webcam frame), the program triggers a left mouse click.

There’s a cooldown of 0.5 seconds so one gesture doesn’t trigger multiple clicks.
