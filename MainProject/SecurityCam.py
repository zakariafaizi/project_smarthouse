import cv2
import winsound


cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Camera number

while cam.isOpened():
    #Capture two instances and compare them
    success, frame1 = cam.read()
    success, frame2 = cam.read()
    # Compare instances to detect the motion
    diff = cv2.absdiff(frame1, frame2)
    # Convert the difference into gray scale
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    # convert gray image  into blur (Brouiller)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # Threshold (Seuil) to get rid of unwanted things
    # Remain only things (Regions) of interest
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    #Dilation is opposite to threshold, it makes things (ROI) bigger
    dilated = cv2.dilate(thresh, None, iterations=3)
    # Contours of ROIs
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Draw contours
    # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 0, 255), 2)
        winsound.PlaySound('alert.wav', winsound.SND_ASYNC)
    # Wait 10 msecs and if the user press 'q' key, break
    if cv2.waitKey(10) == ord('q'):
        break
    # cv2.imshow('Security Camera', diff)
    cv2.imshow('Security Camera', frame1)
