import cv2
import mediapipe as mp
import time
# class handDetector():
#     def __init__(self,mode=False,maxhands=2,detectionCon=0.5,trackCon=0.5):
#         self.mode=mode
#         self.maxhands = maxhands
#         self.detectionCon = detectionCon
#         self.trackCon = trackCon
#
#         self.mphands = mp.solutions.hands
#         self.hands = self.mphands.Hands(self.mode,self.maxhands,self.detectionCon,self.trackCon)
#         self.mpdraw = mp.solutions.drawing_utils
class handDetector():
    def __init__(self, mode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpdraw = mp.solutions.drawing_utils
    def findHands(self,img,draw=True):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb)
        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)
        return img
    def findPosition(self,img,landmarkno=0,handno=0,draw=True):
        lmlist=[]
        if self.results.multi_hand_landmarks:
            myhand=self.results.multi_hand_landmarks[handno]
            for ix, lms in enumerate(myhand.landmark):
                h, w, c = img.shape  # the landmarks is in decimal and we want in pixel so we'll multiply it with height and width
                cx, cy = int(lms.x * w), int(lms.y * h)
                lmlist.append([ix,cx,cy])
                if draw:
                    if ix==landmarkno:
                        cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
        return lmlist

def main():#dummy code which could be run for different projects
    ptime = 0
    ctime = 0

    cap = cv2.VideoCapture(0)

    detect = handDetector()
    landmarkNo=int(input("specify the landmark no"))
    while True:
        success, img = cap.read()
        img=detect.findHands(img)
        lmlist=detect.findPosition(img,landmarkno=landmarkNo)
        if len(lmlist)!=0:
            print(lmlist[landmarkNo])
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)
        cv2.imshow('image', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
if __name__ == "__main__":
    main()