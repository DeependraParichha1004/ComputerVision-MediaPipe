import cv2
import mediapipe as mp
import time
cap=cv2.VideoCapture('video.mp4')
mpface=mp.solutions.face_detection
mpdraw=mp.solutions.drawing_utils
facedetection=mpface.FaceDetection(min_detection_confidence=0.75)
ctime=0
ptime=0
while True:
    success,img=cap.read()
    rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=facedetection.process(rgb)
    # print(results.pose_landmarks)
    if results.detections:
        # print(results.detections)
        for ix,detection in enumerate(results.detections):
            # mpdraw.draw_detection(img, detection)
            # print(ix,detection)
            bboxc=detection.location_data.relative_bounding_box
            h,w,c=img.shape
            bbox=int(bboxc.xmin*w),int(bboxc.ymin*h), \
                 int(bboxc.width * w),int(bboxc.height*h)
            cv2.rectangle(img,bbox,(255,0,255),2)
            cv2.putText(img, f'{int(detection.score[0]*100)}%', (bbox[0],bbox[1]-10), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        # # for poselms in results.pose_landmarks:
        # mpdraw.draw_landmarks(img, results.pose_landmarks, mppose.POSE_CONNECTIONS)
        # for ix,lms in enumerate(results.pose_landmarks.landmark):#results.pose_landmarks is not iterable
        #     h,w,c=img.shape
        #     cx,cy=int(lms.x*w),int(lms.y*h)
        #     cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)
            # print(ix,cx,cy)

    # print(results.pose_landmarks)
    imS = cv2.resize(img, (600,400))

    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(imS,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("img", imS)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break