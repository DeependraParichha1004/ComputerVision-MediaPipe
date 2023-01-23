import cv2
import mediapipe as mp
import time
cap=cv2.VideoCapture('dance.mp4')
mppose=mp.solutions.pose
mpdraw=mp.solutions.drawing_utils
pose=mppose.Pose()
ctime=0
ptime=0
while True:
    success,img=cap.read()
    rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=pose.process(rgb)
    # print(results.pose_landmarks)
    if results.pose_landmarks:
        # for poselms in results.pose_landmarks:
        mpdraw.draw_landmarks(img, results.pose_landmarks, mppose.POSE_CONNECTIONS)
        for ix,lms in enumerate(results.pose_landmarks.landmark):#results.pose_landmarks is not iterable
            h,w,c=img.shape
            cx,cy=int(lms.x*w),int(lms.y*h)
            cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)
            # print(ix,cx,cy)

    # print(results.pose_landmarks)
    imS = cv2.resize(img, (500,600))

    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(imS,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("img", imS)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
