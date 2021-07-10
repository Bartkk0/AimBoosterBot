import keyboard
import mouse
import numpy as np
from PIL import ImageGrab
from cv2 import cv2

X = 182
Y = 383
W = 596
H = 416

while True:
    # Grab a screenshot of the game
    screen = ImageGrab.grab((X, Y, X + W, Y + H)).convert('RGB')
    # Convert it to a numpy array
    img = np.array(screen)
    img = img[:, :, ::-1].copy()

    # Convert the image to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Set the color range
    lower = np.array([0, 0, 0])
    upper = np.array([128, 128, 128])

    # Detect circles and invert the result
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.bitwise_not(mask)

    # Detect contours in the result
    contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    # Check if q is pressed to exit
    if keyboard.is_pressed('q'):
        break

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
