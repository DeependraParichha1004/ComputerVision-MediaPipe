import cv2
import mediapipe as mp
import time
ptime=0
ctime=0
cap=cv2.VideoCapture('video.mp4')
mpfacemesh=mp.solutions.face_mesh
facemesh=mpfacemesh.FaceMesh(max_num_faces=2)
mpdraw=mp.solutions.drawing_utils
drawspec=mpdraw.DrawingSpec(thickness=1,circle_radius=2)
flag = 0
while True:
    success,img=cap.read()
    rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=facemesh.process(rgb)

    if results.multi_face_landmarks:

        for landms in results.multi_face_landmarks:
            # flag=flag+1
            for ix,lms in enumerate(landms.landmark):
                h,w,c=img.shape
                cx,cy=int(lms.x*w),int(lms.y*h)
                print(ix, cx,cy)
            mpdraw.draw_landmarks(img,landms,landmark_drawing_spec=drawspec,connection_drawing_spec=drawspec)

        # print(f'No of detected face: {flag}')




    ims=cv2.resize(img,(500,400))
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(ims, f'fps:{int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv2.imshow("image",ims)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break