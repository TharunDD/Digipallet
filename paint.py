import handrec as htm
import os
import cv2
import mediapipe as mp
import numpy as np
import time
import math

foldp="header";
mylist=os.listdir(foldp);
def main():
   xp=0;
   yp=0;
   brut=15;
   ethk=40;
   print(mylist)
   overlay=[];
   ptime=0
   col=(0,0,255);
   imgcanv=np.zeros((720,1280,3),np.uint8);
   dtr=htm.handTracker();
   for impath in mylist:
      image=cv2.imread(f'{foldp}/{impath}');
      overlay.append(image)
   print(len(overlay));
   header=overlay[0];
   cap = cv2.VideoCapture(0)
   cap.set(3,1280);
   cap.set(4,720);
   tracker = htm.handTracker();
   lmark=[];
   while True:
     success,image = cap.read()
     image=cv2.flip(image,1);
    #  image position
     image[0:117,0:1217]=header
     image = tracker.handsFinder(image);
     lmark=tracker.positionFinder(image);
     if len(lmark)!=0:
      #   print(lmark);
        x1,y1=lmark[8][1:] #tip of index finger;
        x2,y2=lmark[12][1:] #tip of middle finger
        fngers=tracker.fingersup();
      #   print(fngers);
        #selection mode
        if fngers==[1,1,1,1,1]:
            xp=0;
            yp=0;
        else:
         if fngers[1] and fngers[2]:
            xp=0;
            yp=0;
            cv2.rectangle(image,(x1,y1-10),(x2,y2+10),col,cv2.FILLED);
            if y1<117:
               if 612<x1<680:
                  col=(0,255,0);
                  header=overlay[1];
               elif 800<x1<885:
                  col=(255,100,100)
                  header=overlay[3];
               elif 861<x1<968:
                  col=(341,4,255)
                  header=overlay[2];
               elif 923<x1<1020:
                     col=(0,0,0)
                     header=overlay[4];
               elif 525 <x1<590:
                     header=(0,0,255);
                     header=overlay[0]
            print("selection mode");
         #drwa mode
         if fngers[1] == True and fngers[2] == False:
            cv2.circle(image, (x1, y1), 10, col, cv2.FILLED)
            # print("drwaing")
            if xp == 0 and yp == 0:
               xp, yp = x1, y1
            if col==(0,0,0):
               cv2.line(image, (xp, yp), (x1, y1), col, ethk)
               cv2.line(imgcanv, (xp, yp), (x1, y1), col, ethk)       
      # line is used to draw
            cv2.line(image, (xp, yp), (x1, y1), col, brut)
            cv2.line(imgcanv, (xp, yp), (x1, y1), col, brut)
            xp, yp = x1, y1
         else:
               xp,yp=0,0;
     imgg=cv2.cvtColor(imgcanv,cv2.COLOR_BGR2GRAY);
     _,imginv=cv2.threshold(imgg,50,255,cv2.THRESH_BINARY_INV)
     imginv=cv2.cvtColor(imginv,cv2.COLOR_GRAY2BGR);
     image=cv2.bitwise_and(image,imginv);
     image=cv2.bitwise_or(image,imgcanv);
     
     ctime=time.time();
     fps= 1 / (ctime-ptime)
     ptime=ctime
     cv2.putText(image, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)
   #   image=cv2.addWeighted(image,0.5,imgcanv,0.5,0)
     cv2.imshow("Video",image)
     cv2.imshow("imcancx",imgcanv);
     cv2.waitKey(1)
if __name__ == "__main__":
  main()