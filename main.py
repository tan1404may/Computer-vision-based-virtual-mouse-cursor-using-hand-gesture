import handtacking as ht
import cv2
import numpy as np
import time
import tkinter
import mouse
import keyboard
import pyperclip



# pip install opencv-python
# pip install mediapipe
# pip install numpy
# pip install tk 
# pip install mouse
# pip install keyboard
# pip install pyperclip







#######################################
root = tkinter.Tk()
wCam=500
hCam=500
wScr, hScr = root.winfo_screenwidth(), root.winfo_screenheight()
framer = 50 # frame reduction
smoothening = 10
prevX, prevY = 0, 0
curX, curY = 0, 0

# to calculate frame rate
prevtime = 0
currtime = 0 
########################################


# read video stream
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = ht.HandTracker()


while(True):
    # extract image from video
    success, image = cap.read()

    imageRGB = detector.find_hands(image)  
    # print(detector.find_position(imageRGB))

    landmarks = detector.find_position(imageRGB)

    try:
        # to do something
        if(len(landmarks) != 0):
            x1, y1 = landmarks[8][1:]
            x2, y2 = landmarks[12][1:]

            fingers = detector.fingers_up()
            # need to create a range to detect, instead of working on entire image
            cv2.rectangle(imageRGB, (framer, framer), (wCam-framer, hCam-framer), 
                                            (255, 0, 0), 3)


            # [thumb, index, middle, ring, pinky]
            # move cursor
            if(fingers == [0,1,0,0,0]):

                x3 = np.interp(x1, (framer, wCam-framer), (0, wScr))      
                y3 = np.interp(y1, (framer, hCam-framer), (0, hScr))      
                

                # smoothen value a bit
                curX = prevX + (x3 - prevX) / smoothening
                curY = prevY + (y3 - prevY) / smoothening

                # autopy.mouse.move(wScr-curX, curY)
                mouse.move(wScr-curX, curY)
                cv2.circle(imageRGB,(x1, y1), 15, (255, 0, 255), cv2.FILLED)
                prevX, prevY = curX, curY


            # click action
            if (fingers == [1, 1, 1, 0 ,0]):
                lenght1, img, lineinfo = detector.find_distance(8, 12, imageRGB)
                length2, img, lineinfo = detector.find_distance(8, 4, imageRGB)
                
                # right click
                # index or middle fingre
                if(lenght1 < 30):
                    cv2.circle(img, (lineinfo[4], lineinfo[5]), 15, (0,255,0), cv2.FILLED)
                    # autopy.mouse.click('RIGHT')
                    mouse.click('right')
                    print('right click')

                # left click
                # index or thumb
                if (length2 < 30):
                    cv2.circle(img, (lineinfo[4], lineinfo[5]), 15, (0,255,0), cv2.FILLED)
                    # autopy.mouse.click()
                    mouse.click('left')
                    print("left click")

                
            # scroll action : only pinky up
            if(fingers == [0,0,0,0,1]):
                mouse.wheel(1)

            # for down scroll : index and pinky up
            if (fingers == [0, 1, 0, 0, 1]):
                mouse.wheel(-1)


            # copy things up index, middle, ring
            if(fingers == [0, 1, 1, 1, 0]):
                # copy thing
                print("cut operation performed")
                keyboard.send('ctrl+c')
                
                
            # paste things: up index, middle
            if(fingers == [0, 0, 1, 1, 0]):
                print("paste operation performed")
                keyboard.send('ctrl+v') 
                pyperclip.copy('')




    except:
        continue

        
    currtime = time.time()
    fps = 1 / (currtime - prevtime)
    prevtime = currtime
    cv2.putText(imageRGB, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 2)
    cv2.imshow("image", imageRGB)
    # cv2.imshow("image", imageRGB)

    # press escape key to quit
    if(cv2.waitKey(1) == 27):
        cap.release()
        cv2.destroyAllWindows()
        break


