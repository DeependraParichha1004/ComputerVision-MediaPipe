import cv2
import mediapipe as mp
import time
import math
import numpy as np
import posedetectormodule as pdm
cap=cv2.VideoCapture('curls_video.mp4')
detector=pdm.poseDetector()
count=0
dir=1
while True:
    success, img = cap.read()
    # img = cv2.imread('curls_pic.jpg')
    img=cv2.resize(img,(580,540))
    detector.findPose(img,False)
    lmlist=detector.findPosition(img,False)
    if len(lmlist)!=0:
        angle=detector.findAngle(img,11,13,15,True)
        per=np.interp(angle,(225,270),(0,100))
        # print(angle,per)

        # detector.findAngle(img,12,14,16,True)
        if per==100:
            if dir==1:
                count+=0.5
                dir=0
        if per==0:
            if dir==0:
                count+=0.5
                dir=1
        print(count)
        cv2.putText(img,str(f'{count}'),(150,200),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)

    cv2.imshow("image",img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break