import cv2
import mediapipe as mp
import time
import numpy as np
import handdetectormodule as hdm
import math
ptime=0
ctime=0
cap=cv2.VideoCapture(0)

mpfacemesh=mp.solutions.face_mesh
facemesh=mpfacemesh.FaceMesh(max_num_faces=2)
mpdraw=mp.solutions.drawing_utils
drawspec=mpdraw.DrawingSpec(thickness=1,circle_radius=2)
flag = 0
detector=hdm.handDetector()
vol=0
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
print(volume.GetVolumeRange())

minvol=volume.GetVolumeRange()[0]
maxvol=volume.GetVolumeRange()[1]
volbar=400
per=0
while True:
    success,img=cap.read()
    img=detector.findHands(img)
    landms=detector.findPosition(img,draw=False)
    if len(landms)!=0:
        # print(landms[4],landms[8])
        x1,y1=landms[4][1],landms[4][2]
        x2,y2=landms[8][1],landms[8][2]
        cv2.circle(img,(x1,y1),20,(0,255,0),cv2.FILLED)
        cv2.circle(img,(x2,y2),20,(0,255,0),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)
        cv2.circle(img, ((x1+x2)//2, (y1+y2)//2), 20, (0, 0, 255), cv2.FILLED)
        length=math.hypot(x2-x1,y2-y1)
        vol=np.interp(length,[50,300],[minvol,maxvol])
        per=np.interp(length,[50,300],[0,100])
        volbar=np.interp(length,[50,300],[400,150])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)
    cv2.rectangle(img,(50,150),(80,400),(255,0,0),3)
    cv2.rectangle(img,(50,int(volbar)),(80,400),(255,0,0),cv2.FILLED)
    cv2.putText(img, f'{int(per)}%', (50, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        # cv2.rectangle(img,[50,80],(255,0,0),3)
        # print(math.hypot(x2-x1,y2-y1))
    # rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    # rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # results=facemesh.process(rgb)
    #
    # if results.multi_face_landmarks:
    #
    #     for landms in results.multi_face_landmarks:
    #         # flag=flag+1
    #         for ix,lms in enumerate(landms.landmark):
    #             h,w,c=img.shape
    #             cx,cy=int(lms.x*w),int(lms.y*h)
    #             print(ix, cx,cy)
    #         mpdraw.draw_landmarks(img,landms,landmark_drawing_spec=drawspec,connection_drawing_spec=drawspec)
    #
    #     # print(f'No of detected face: {flag}')
    #



    ims=cv2.resize(img,(500,400))
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(ims, f'fps:{int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv2.imshow("image",ims)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break