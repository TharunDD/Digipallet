import cv2
import mediapipe as mp
import numpy as np
import time
import math
class handTracker():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.85,modelComplexity=1,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipid=[4,8,12,16,20]
    def handsFinder(self,image,draw=True):
        imageRGB = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image
    def positionFinder(self,image, handNo=0, draw=False):
       self.lmlist = []
       if self.results.multi_hand_landmarks:
           Hand = self.results.multi_hand_landmarks[handNo]
           for id, lm in enumerate(Hand.landmark):
               h,w,c = image.shape
               cx,cy = int(lm.x*w), int(lm.y*h)
               self.lmlist.append([id,cx,cy]);
       return self.lmlist
    def fingersup(self):
        fingers =[];
        if self.lmlist[self.tipid[0]][1]<self.lmlist[self.tipid[0]-1][1]:
            fingers.append(1);
        else:
            fingers.append(0)
        for id in range(1,5):
             if self.lmlist[self.tipid[id]][2]<self.lmlist[self.tipid[id]-2][2]:
                fingers.append(1);
             else:
                fingers.append(0)
        return fingers;            
# def main():
#  cap = cv2.VideoCapture(0)
#  tracker = handTracker();
#  volbar=0;
#  volper=0;
#  ptime=0;
#  while True:
#      success,image = cap.read()
#      image = tracker.handsFinder(image)
#      lmList = tracker.positionFinder(image)
#      ctime=time.time();
#      fps= 1 / (ctime-ptime)
#      ptime=ctime
#      cv2.putText(image, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)
#      cv2.imshow("Video",image)
#      cv2.waitKey(1)
# if __name__ == "__main__":
#   main()