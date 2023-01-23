import cv2
import mediapipe as mp
import time
cap=cv2.VideoCapture(0)

ctime=0
ptime=0

mphands=mp.solutions.hands
hands=mphands.Hands()
mpdraw=mp.solutions.drawing_utils
while True:
    success,img=cap.read()
    rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(rgb)
    # print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:#results.multi_hand_landmarks is iterable(because of list)
            for ix,lms in enumerate(handlms.landmark):
                # print(ix,lms)
                h,w,c=img.shape#the landmarks is in decimal and we want in pixel so we'll multiply it with height and width
                cx,cy=int(lms.x*w),int(lms.y*h)
                # print(ix,cx,cy)
                if ix==8:
                    cv2.circle(img,(cx,cy),25,(255,0,255),cv2.FILLED)
            mpdraw.draw_landmarks(img,handlms,mphands.HAND_CONNECTIONS)
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img,str(int(fps)),(10,50),cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),3)
    cv2.imshow('image',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break