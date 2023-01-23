import cv2
import time
import mediapipe as mp
import math
import handtrackingmodule as htm
import numpy as np
import osascript


pTime = 0
Cap = cv2.VideoCapture(0)
detector = htm.handDetector()


while True:
    success, img = Cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        print(lmList[4],lmList[8])
   #print(lmList[4][1])
        x1 , y1 = lmList[4][1] , lmList[4][2]
        x2 , y2 = lmList[8][1] , lmList[8][2]
        cx , cy =  (x1+x2)/2 , (y1+y2)/2

        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        length = math.hypot(x2-x1,y2-y1)
        vol = np.interp(length,[50,500],[0,100])
        vol1 = "set volume output volume " + str(vol)
        osascript.osascript(vol1)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'fps:{int(fps)}',(20,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),1)

    cv2.imshow('image',img)
    cv2.waitKey(1)