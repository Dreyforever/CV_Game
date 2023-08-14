import math
import cv2
import HandTrackingModule as htm
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3,1080)
cap.set(4,720)

detector = htm.HandDetector(detectionCon=0.7, maxHands=1)

x = [300,245,200,170,145,130,112,103,93,87,80,75,70,67,62,59,57]
y = [20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
coeff = np.polyfit(x,y,2)


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:

        x1, y1 = lmList[5][1], lmList[5][2]
        x2, y2 = lmList[17][1], lmList[17][2]
        length = math.hypot(x2-x1,y2-y1)
        # print(length)
        ycm = coeff[0] * length * length + coeff[1] * length + coeff[2]
        # print(ycm)
        cv2.putText(img, f'{int(ycm)} cm', (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)