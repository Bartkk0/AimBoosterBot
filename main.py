import time

import keyboard
import mouse
import numpy as np
from PIL import ImageGrab
from cv2 import cv2

X = 182
Y = 369
W = 596
H = 416

SLEEP_AFTER_CLICK = 0.1
SLEEP_AFTER_ITER = 0.3

while True:
    # Check if q is pressed to exit
    if keyboard.is_pressed('q'):
        break

    # Check if e is pressed to pause
    if keyboard.is_pressed('e'):
        continue

    # Grab a screenshot of the game
    screen = ImageGrab.grab((X, Y, X + W, Y + H)).convert('RGB')
    # Convert it to a numpy array
    img = np.array(screen)
    img = img[:, :, ::-1].copy()

    # Convert the image to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Set the color range
    lower = np.array([23 / 2, (23 / 100) * 255, (100 / 100) * 255])
    upper = np.array([25/2, (70/100)*255, (100/100)*255])

    # Detect circles and invert the result
    mask = cv2.inRange(hsv, lower, upper)

    # Detect contours in the result
    contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    for c in contours:
        # Check the contour area
        area = cv2.contourArea(c)
        if area < 100:
            continue

        # Calculate the center of the contour
        center = cv2.moments(c)
        if center["m00"] == 0:
            continue

        centerX = int(center["m10"] / center["m00"])
        centerY = int(center["m01"] / center["m00"])

        # Move the mouse and click
        mouse.move(X + centerX, Y + centerY)
        mouse.click('left')

        time.sleep(SLEEP_AFTER_CLICK)

    time.sleep(SLEEP_AFTER_ITER)
