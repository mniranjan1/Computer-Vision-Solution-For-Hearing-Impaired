# organize imports
import cv2
import numpy as np
import os
import imutils
from script import run_avg, segment

IMG_SIZE = 256
aWeight = 0.5


def init_create_folder():
    # create the folder and database if not exist
    if not os.path.exists("gestures"):
        os.mkdir("gestures")


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)


def store_images(g_id):
    # region of interest (ROI) coordinates
    top, right, bottom, left = 100, 350, 400, 650

    camera = cv2.VideoCapture(0)
    total_pics = 2000
    pic_no = 0
    flag_start_capturing = False
    frames = 0
    create_folder("gestures/"+str(g_id))
    while(True):
        (t, frame) = camera.read()

        frame = imutils.resize(frame, width=700)
        # flip the frame so that it is not the mirror view
        frame = cv2.flip(frame, 1)

        clone = frame.copy()

        # get the ROI
        roi = frame[top:bottom, right:left]

        # convert the roi to grayscale and blur it
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        # resize img
        gray = cv2.resize(gray, (IMG_SIZE, IMG_SIZE))

        if frames < 20:
            run_avg(gray, aWeight)
        else:
         # segment the hand region
            hand = segment(gray)
        # check whether hand region is segmented
            if hand is not None:
                # if yes, unpack the thresholded image and
                # segmented region
                (thresholded, segmented, tour) = hand

            # draw the segmented region and display the frame
                cv2.drawContours(
                    clone, [segmented + (right, top)], -1, (0, 0, 255))
                cv2.imshow("Thesholded", thresholded)

                if frames > 150:
                    cv2.imwrite("gestures/"+str(g_id)+"/" +
                                str(pic_no)+".jpg", thresholded)

                    pic_no += 1
                    st = int((pic_no)*100/total_pics)
        # draw the segmented hand
                    cv2.putText(frame, "Capturing..." + str(st) + " %", (30, 60),
                                cv2.FONT_HERSHEY_TRIPLEX, 1, (127, 255, 255))
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.imshow("Video Feed 1", gray)

        cv2.imshow("Video Feed", frame)
        # observe the keypress by the user)

        # if the user pressed "Esc", then stop looping
        keypress = cv2.waitKey(1)
        if keypress == ord('q'):
            break
        if keypress == ord('c'):
            if flag_start_capturing == False:
                flag_start_capturing = True
            else:
                flag_start_capturing = False
                frames = 0
        if flag_start_capturing == True:
            frames += 1
        if pic_no == total_pics:
            break


init_create_folder()
g_id = input("Enter gesture no.: ")
g_name = input("Enter gesture name/text: ")
store_images(g_id)
