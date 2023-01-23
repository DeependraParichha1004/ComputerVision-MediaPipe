# import handdetectormodule as hdm
# import cv2
# import os
# import numpy as np
# import mediapipe as mp
# import time
# cap=cv2.VideoCapture(0)
# ptime=0
# ctime=0
# mylist=os.listdir('images')
# print(mylist)
# list=[]
# for img in mylist:
#     img=cv2.imread(f'images/{img}')
#     list.append(img)
# print(list[1].shape)
# detector=hdm.handDetector()
# ids=[4,8,12,16,20]
# while True:
#     success,img=cap.read()
#     img=detector.findHands(img)
#     lmlist=detector.findPosition(img)
#     # h, w, c = list[0].shape
#     if len(lmlist)!=0:
#         fingers=[]
#         #thumb
#         if lmlist[ids[0]][1]<lmlist[ids[0]-1][1]:
#             fingers.append(0)
#
#         else:
#             fingers.append(1)
#         #fingers
#         for i in range(1,5):
#             if lmlist[ids[i]][2]<lmlist[ids[i]-2][2]:
#                 fingers.append(1)
#
#             else:
#                 fingers.append(0)
#         fingersno=fingers.count(1)
#         print(fingersno)
#         h, w, c = list[fingersno-1].shape
#         img[0:h, 0:w] = list[fingersno-1]
#         print(fingers)
#
#
#     ctime=time.time()
#     fps=1/(ctime-ptime)
#     ptime=ctime
#     cv2.putText(img,str(int(fps)),(10,50),cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),3)
#     cv2.imshow('image',img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

import cv2
import time
import numpy as np
import os
import handdetectormodule as htm

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "images"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    # print(f'{folderPath}/{imPath}')
    image=cv2.resize(image,(280,200))
    overlayList.append(image)
# print(overlayList.shape)
print(len(overlayList))
pTime = 0

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)

    if len(lmList) != 0:
        fingers = []

        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)

        h, w, c = overlayList[totalFingers-1].shape
        print(h,w)
        # img = cv2.resize(img, (640, 480))
        print(np.array(overlayList).shape)
        img[0:h, 0:w] = overlayList[totalFingers-1]

        cv2.rectangle(img, (20, 275), (150, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    5, (255, 0, 0), 10)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
#no thumb
#only index finger