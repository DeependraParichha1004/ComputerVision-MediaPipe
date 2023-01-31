import cv2
import mediapipe as mp
import time
import os
import numpy as np
import handdetectormodule as hdm
mylist=os.listdir("header")
ptime=0
ctime=0
color=(255,0,255)
# print(mylist)
overlaylist=[]
for file in mylist:

    img=cv2.imread(f'{"header"}/{file}')
    img = cv2.resize(img, (640,100))
    overlaylist.append(img)
print(len(overlaylist))
cap=cv2.VideoCapture(0)
width = 640
height = 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
detector=hdm.handDetector(detectionCon=0.75)
header=overlaylist[0]
xp,yp=0,0
imgcanvas=np.zeros((480,640,3),np.uint8)
while True:
    success,img=cap.read()
    img=cv2.flip(img,1)
    hands=detector.findHands(img)
    handlms=detector.findPosition(img,draw=False)
    if len(handlms)!=0:
        # print(handlms)

        fingers=detector.fingersup()
        # print(fingers)

        if fingers[1] and fingers[2]:
            x1,y1=handlms[8][1],handlms[8][2]
            x2,y2=handlms[12][1],handlms[12][2]

            if y1<100:
                if 30<x1<160:
                    header=overlaylist[0]
                    color=(255,0,255)
                elif 180<x1<320:
                    header=overlaylist[1]
                    color=(255,0,0)
                elif 350 < x1 < 530:
                    header = overlaylist[2]
                    color=(0,255,0)
                elif 560 < x1 < 640:
                    header = overlaylist[3]
                    color=(0,0,0)
            cv2.circle(img, (x1, y1), 15, color, cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, color, cv2.FILLED)
            print("selection")
        if fingers[1] and fingers[2]==False:
            x1, y1 = handlms[8][1], handlms[8][2]
            cv2.circle(img, (x1, y1), 15, color, cv2.FILLED)
            if xp==0 and yp==0:
                xp,yp=x1,y1
            elif color==(0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), color, 100)
                cv2.line(imgcanvas, (xp, yp), (x1, y1), color, 100)
            else:
                cv2.line(img,(xp,yp),(x1,y1),color,10)
                cv2.line(imgcanvas,(xp,yp),(x1,y1),color,10)
            xp,yp=x1,y1
            print("click")

    imggray=cv2.cvtColor(imgcanvas,cv2.COLOR_BGR2GRAY)
    _, imginv = cv2.threshold(imggray, 50, 255, cv2.THRESH_BINARY_INV)
    imginv = cv2.cvtColor(imginv, cv2.COLOR_GRAY2BGR)
    img=cv2.bitwise_and(img,imginv)
    img=cv2.bitwise_or(img,imgcanvas)
    h,w,c=overlaylist[0].shape
    img[0:h,0:w]=header
    # img=cv2.addWeighted(img,0.5,imgcanvas,0.5,0)
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)
    cv2.imshow('image',img)
    # cv2.imshow('imagecanvas',imgcanvas)
    # cv2.imshow('imggray',imggray)
    cv2.imshow('imginv',imginv)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

