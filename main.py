import handtacking as ht
import cv2
import numpy as np
import time
import autopy
import mouse
import keyboard



#######################################
wCam=500
hCam=500
wScr, hScr = autopy.screen.size()
framer = 100 # frame reduction
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
            if(fingers[1] == 1 and fingers[0]==0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0):

                x3 = np.interp(x1, (framer, wCam-framer), (0, wScr))      
                y3 = np.interp(y1, (framer, hCam-framer), (0, hScr))      
                

                # smoothen value a bit
                curX = prevX + (x3 - prevX) / smoothening
                curY = prevY + (y3 - prevY) / smoothening

                autopy.mouse.move(wScr-curX, curY)
                cv2.circle(imageRGB,(x1, y1), 15, (255, 0, 255), cv2.FILLED)
                prevX, prevY = curX, curY


            # click action
            if (fingers[1]==1 and fingers[2]==1 and fingers[0]==1 and fingers[3]==0 and fingers[4]==0):
                lenght1, img, lineinfo = detector.find_distance(8, 12, imageRGB)
                length2, img, lineinfo = detector.find_distance(8, 4, imageRGB)
                
                # right click
                # index or middle fingre
                if(lenght1 < 40):
                    cv2.circle(img, (lineinfo[4], lineinfo[5]), 15, (0,255,0), cv2.FILLED)
                    # autopy.mouse.click('RIGHT')
                    mouse.click('right')
                    print('right click')
                
                # left click
                # index or thumb
                if (length2 < 40):
                    cv2.circle(img, (lineinfo[4], lineinfo[5]), 15, (0,255,0), cv2.FILLED)
                    # autopy.mouse.click()
                    mouse.click('left')
                    print("left click")

                
            # scroll action
            # if(condition):
            #     # check if for up scroll
            #     if(condition):
            #         mouse.wheel(1)



            #     for down scroll
            #     if (condition):
            #         mouse.wheel(-1)



            # # cut things : all fingers are down
            # if(fingers[0]==0 and fingers[1]==0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0):
            #     # copy thing
            #     print("cut operation performed")
            #     keyboard.send('ctrl+x')
                
                
            # # # paste things : all fingers are up
            # if(fingers[0]==1 and fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==1):
            #     print("paste operation performed")
            #     keyboard.send('ctrl+v') 


            
            # change window
            # if(condition):
            #     keyboard.send('alt+tab')



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


