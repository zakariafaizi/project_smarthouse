import face_recognition
import os
from time import sleep
import ctypes
import numpy as np
from datetime import datetime
# Pronounce
import googletrans
import speech_recognition as sr
import gtts
import playsound
from pyzbar.pyzbar import decode
from prettytable import PrettyTable

recognizer = sr.Recognizer()
translator = googletrans.Translator()
input_lang = 'en-US'
output_lang = 'en'
import pymongo as mongo
import winsound
import cv2



# define the list of boundaries
colors_names = ['black','blue','red','green','orange','yellow','purple']
colors_lower = [[0, 0, 0],[100, 100,100],[0, 100, 100],[42, 100, 100],[13, 100, 100],[25, 100, 100],[135,100,100]]
colors_upper = [[112, 255, 55],[131, 255, 255],[7, 255, 255],[75,255, 255],[20,255, 255],[30, 255, 255],[146,255,255]]


myclient = mongo.MongoClient("mongodb+srv://zakariafaizi:projetpfc123@clusterpfc.efa6c.mongodb.net/FaceRecognition")
mydb = myclient["FaceRecognition"]
people = mydb["project"]


path = "ImagesBasic"

images = []

classNames = []  # images' names

myList = os.listdir(path)

inconnu = 1

for img in myList:
    currentImg = cv2.imread(f'{path}/{img}')
    rgb = cv2.cvtColor(currentImg, cv2.COLOR_BGR2RGB)
    images.append(rgb)  # image matrix
    classNames.append(os.path.splitext(img)[0])  # name

def showMessage(text,title):
    return ctypes.windll.user32.MessageBoxW(0, text, title, 1)

def updateCSV():
    myDataList = list()
    for x in people.find():
        myDataList.append(x)

    t = PrettyTable(['Name', 'Counter', 'Color', 'Arrival', 'Departure'])
    t.align = 'l'
    t.border = False

    with open('Attendance.csv', 'r+') as f:
        f.truncate(0)
        for j in range(len(myDataList)):
            t.add_row([myDataList[j]["name"], myDataList[j]["count"],myDataList[j]["color"] ,myDataList[j]["timein"], myDataList[j]["timeout"]])
        f.write(t.get_string(border=True))

def findEncoding(imgs):
    encodeList = []
    for img in imgs:
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


encodeListFinal = findEncoding(images)

cam = cv2.VideoCapture(0)


colorIterator = 0
def colorDetect():
    while True:
        global colorIterator
        _, frame = cam.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array(colors_lower[colorIterator]), np.array(colors_upper[colorIterator]))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if colorIterator == 5:
            colorIterator = 0
        else:
            colorIterator += 1
        for c in contours:
            area = cv2.contourArea(c)
            if area > 30000:
                color = colors_lower.index(colors_lower[colorIterator - 1])
                color = colors_names[color]
                return color


def markAttendance(name):
    actual = people.find({"name": name})[0]
    # retrieve existing name
    myDataList = list()
    for x in people.find():
        myDataList.append(x)

    peoplenames = list()
    for j in range(len(myDataList)):
        peoplenames.append(myDataList[j]['name'])

    cnt = actual['count']

    if int(cnt) < 1:
        now = datetime.now()
        dtString = now.strftime('%A %d %B at %H:%M')
        print("Welcome " + name)
        people.update_one({"name": name}, {"$set": {"count": 1, "timein": dtString}})
        updateCSV()

    else:
        if int(cnt) % 2:
            print("Bye ", name)
            now = datetime.now()
            dtString = now.strftime('%A %d %B at %H:%M')
            RecognizedCounter = people.find({"name" : name})[0]
            RecognizedCounter = RecognizedCounter["count"]
            people.update_one({"name" : name} , {"$set":{"count":str(int(RecognizedCounter)+1),"timeout":dtString}})
            updateCSV()

        else:
            print("Welcome ", name)
            now = datetime.now()
            dtString = now.strftime('%A %d %B at %H:%M')
            RecognizedCounter = people.find({"name": name})[0]
            RecognizedCounter = RecognizedCounter["count"]
            people.update_one({"name": name}, {"$set": {"count": str(int(RecognizedCounter) + 1), "timein": dtString , "timeout":"---"}})
            updateCSV()




nomQRG = ""
while cam.isOpened():
    success, frame = cam.read()
    success, frame2 = cam.read()
    frame = cv2.flip(frame, 1)
    frame2 = cv2.flip(frame2,1)
    # compare two instances to detect the motion
    diff = cv2.absdiff(frame, frame2)

    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # blur image
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # threshold to get rid of unwanted objects
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    # contours of ROI's       # ROI = REGION OF INTEREST
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv2.contourArea(c) > 5000:
            imgRs = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
            imgRs = cv2.cvtColor(imgRs, cv2.COLOR_BGR2RGB)

            if len(nomQRG) < 1:
                # detect QR code
                for QR in decode(imgRs):
                    nomQR = QR.data.decode()
                    print("nomQR : ", nomQR)
                    nomQRG = nomQR
                    break;

            elif len(nomQRG) > 1:
                sleep(1)
                facesloc = face_recognition.face_locations(imgRs)  # faces
                encodeFaces = face_recognition.face_encodings(imgRs, facesloc)
                for encodeFace, faceloc in zip(encodeFaces, facesloc):
                    results = face_recognition.compare_faces(encodeListFinal, encodeFace)  # returns true or false
                    faceDist = face_recognition.face_distance(encodeListFinal, encodeFace)  # returns distance ...
                    facedistIndex = np.argmin(faceDist)  # returns lower distance index
                    if results[facedistIndex]:  # if results[index] == True
                        name = classNames[facedistIndex]

                        if name == nomQRG:
                            markAttendance(name)
                            nomQRG = ""
                            break
                        elif name != nomQRG:
                            showMessage("SHOW YOUR COLOR CARD PLEASE !", "Message")
                            sleep(2)
                            colorShown = colorDetect()
                            print("color shown",colorShown)
                            x = people.find({"name": nomQRG})[0]
                            RealColor = x['color']
                            print("RealColor" , RealColor)
                            if colorShown == RealColor:
                                markAttendance(nomQRG)
                                nomQRG = ""
                                break
                            else:
                                print("Stranger")
                                winsound.PlaySound('alert.wav', winsound.SND_ASYNC)
                                nomQRG = ""
                                break


                    else:
                        print("Stranger2")
                        winsound.PlaySound('alert.wav', winsound.SND_ASYNC)
                        nomQRG = ""
                        break




    if cv2.waitKey(10) == ord('q'):
        break
    cv2.imshow('Security camera ', frame)

cam.release()