import cv2
import numpy as np
import pyautogui

# orange_lower = np.array([10, 10, 140])
# orange_upper = np.array([60,5, 150])

blue_lower = np.array([80, 75, 63])
blue_upper = np.array([112, 239, 255])


black_lower = np.array([22, 0, 43])
black_upper = np.array([177, 96, 93])

prev_y = 0
'''Number1'''
cap = cv2.VideoCapture(0)
while True:
    _ , frame = cap.read()
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, blue_lower, blue_upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    for c in contours:
        area = cv2.contourArea(c)
        if area > 5000:
             #cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(c)
            #print(x, y, w, h)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            if y < prev_y-100:
                 pyautogui.press('pageup')
                 print("go up")
            elif y > prev_y+100:
                pyautogui.press('pagedown')
                print("go down")
            else: continue
            prev_y = y
    cv2.imshow('Frame', frame)
    #cv2.imshow('Gray Image', gray)
    if cv2.waitKey(10) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
