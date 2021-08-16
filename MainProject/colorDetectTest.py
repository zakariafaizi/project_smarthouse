# import the necessary packages
import numpy as np
import argparse
import cv2



blue_lower = np.array([100, 100,100])
blue_upper = np.array([131, 255, 255])

red_lower = np.array([0, 100, 100])
red_upper = np.array([7, 255, 255])

green_lower = np.array([42, 100, 100])
green_upper = np.array([75,255, 255])

orange_lower = np.array([13, 100, 100])
orange_upper = np.array([20,255, 255])

yellow_lower = np.array([25, 100, 100])
yellow_upper = np.array([30, 255, 255])

black_lower = np.array([0, 0, 0])
black_upper = np.array([112, 255, 55])


# define the list of boundaries
colors_names = ['blue','red','green','orange','yellow','black']
colors_lower = [[100, 100,100],[0, 100, 100],[42, 100, 100],[13, 100, 100],[25, 100, 100],[0, 0, 0]]
colors_upper = [[131, 255, 255],[7, 255, 255],[75,255, 255],[20,255, 255],[30, 255, 255],[112, 255, 55]]


cam = cv2.VideoCapture(0)

i = 0


while True:
    _,frame = cam.read()
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array(colors_lower[i]), np.array(colors_upper[i]))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if i == 5:
        i = 0
    else:
        i += 1
    for c in contours:
        area = cv2.contourArea(c)
        if area > 20000:
            # cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(c)
            #card = frame[x:x+w,y:y+h]
            #meancolor = card.mean(2)
            # print(x, y, w, h)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            print("i",i)
            color = colors_lower.index(colors_lower[i-1])
            color = colors_names[color]
            print(color)


    if cv2.waitKey(10) == ord('q'):
        break
    cv2.imshow('Security camera ', frame)