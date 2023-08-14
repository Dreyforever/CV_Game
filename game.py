import math
import random
import time
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

# enabling the camera and setting the resolution
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

# defining the HandDetector that will be used for the program
detector = HandDetector(detectionCon=0.7, maxHands=1)

# x is the distance that has been calculated by the program and y is the real life distance from the camera
x = [300,245,200,170,145,130,112,103,93,87,80,75,70,67,62,59,57]
y = [20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]

# Need to do non-linear fitting between the two (as their relation is a non-linear polynomial of degree 2)
coeff = np.polyfit(x,y,2)

# Defining the game variables
cx, cy = 250 , 250
color = (255, 0, 255)
score = 0
counter = 0

# defining the StartTime and the total time that the game will run for
StartTime = time.time()
GameTime = 20

while True:
    success, img = cap.read()
    img = cv2.flip(img,1)

    # setting up the timer for the game
    if time.time()-StartTime < GameTime:
        hands, img = detector.findHands(img)
        if hands:
            lmList = hands[0]['lmList']
            x, y, w, h = hands[0]['bbox']
            x1, y1 = lmList[5][0], lmList[5][1]
            x2, y2 = lmList[17][0], lmList[17][1]

            # Here, length is the distance between the bottom of the index and little finger
            length = math.hypot(x2-x1,y2-y1)

            # using the coefficients btained from the polyfit to find the relation between the calculated length and real-life distance from the camera
            ycm = coeff[0] * length * length + coeff[1] * length + coeff[2]
            cv2.putText(img, f'{int(ycm)} cm', (60, 150), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

            # defining the distance at which the button click will be registered. 
            # The bounding box of the hand has to be enclosing the button to be considered as a successful click
            if ycm < 40:
                if x < cx < x+w and y < cy < y + h:
                    counter = 1

        # calculating the score
        if counter:
            counter+= 1
            color = (0, 255, 0)
            if counter == 4:
                cx = random.randint(100, 1100)
                cy = random.randint(100, 650)
                color = (255, 0, 255)
                score += 1
                counter = 0

        # creating the button
        cv2.circle(img, (cx,cy), 20, color, cv2.FILLED)
        cv2.circle(img, (cx,cy), 7, (255,255,255), cv2.FILLED)
        cv2.circle(img, (cx,cy), 13, (255,255,255), 2)
        cv2.circle(img, (cx,cy), 20, (50,50,50), 2)

        # Creating Game GUI
        cvzone.putTextRect(img, f'Time : {int(GameTime-time.time()+StartTime)}', (1000,75), scale=3, offset = 20)
        cvzone.putTextRect(img, f'Points : {score}', (60, 75), scale=3, offset = 20)

    else:
        # displaying the EndGame screen
        cvzone.putTextRect(img, f'Game Over', (400, 400), scale=5, offset = 30)
        cvzone.putTextRect(img, f'Points : {score}', (450, 500), scale=4, offset=20)
        cvzone.putTextRect(img, f'Press R to play again', (400, 680), scale=2.5, offset=20)

    cv2.imshow("Img", img)
    key = cv2.waitKey(1)

    # enabling the play again option
    if key == ord('r'):
        StartTime = time.time()
        score = 0
