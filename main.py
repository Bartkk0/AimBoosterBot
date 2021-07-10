import sys
import time

import mouse
import keyboard
from cv2 import cv2
from PIL import Image
from PIL import ImageGrab
import numpy as np
import pyautogui as pag

X = 182
Y = 383
W = 596
H = 416

while True:
    screen = ImageGrab.grab((X, Y, X + W, Y + H)).convert('RGB')
    img = np.array(screen)
    img = img[:, :, ::-1].copy()

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 0, 0])
    upper = np.array([128, 128, 128])

    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.bitwise_not(mask)

    contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    if keyboard.is_pressed('q'):
        break

    result = img.copy()
    for c in contours:
        area = cv2.contourArea(c)

        if area < 100:
            continue

        center = cv2.moments(c)
        if center["m00"] == 0:
            continue

        centerX = int(center["m10"] / center["m00"])
        centerY = int(center["m01"] / center["m00"])

        # print(f"Center {centerY} {centerY}")
        mouse.move(X + centerX, Y + centerY)
        #mouse.click('left')
        #pag.click()
