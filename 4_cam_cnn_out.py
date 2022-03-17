import numpy as np
import imutils
import cv2        # dealing with arrays
import os                  # dealing with directories
import math
from script import run_avg, segment
from tensorflow.keras.models import Sequential, load_model
import pyttsx3
from threading import Thread

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
engine = pyttsx3.init()
engine.setProperty('rate', 150)

IMG_SIZE = 256


MODEL_NAME = 'handsign1.h5'

model = load_model(MODEL_NAME)
print('model loaded!')


# organize imports

out_label = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
             'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'space', 'del', 'Love', 'Remember', 'Best of Luck', 'You', 'Rock', 'Like']
pre = []
text = ""
word = ""
cchar = [0, 0]
c1 = ''

# initialize weight for running average
aWeight = 0.5

# get the reference to the webcam,
camera = cv2.VideoCapture(0)

# region of interest (ROI) coordinates
top, right, bottom, left = 100, 350, 400, 650

# initialize num of frames
num_frames = 0
count_same_frame = 0


def say_text(text):
    if not is_voice_on:
        return
    while engine._inLoop:
        pass
    engine.say(text)
    engine.runAndWait()


is_voice_on = True
# keep looping, until interrupted
while(True):
    # get the current frame
    (grabbed, frame) = camera.read()

    # resize the frame
    frame = imutils.resize(frame, width=700)

    # flip the frame so that it is not the mirror view
    frame = cv2.flip(frame, 1)

    # clone the frame
    clone = frame.copy()

    # get the height and width of the frame
    (height, width) = frame.shape[:2]

    # get the ROI
    roi = frame[top:bottom, right:left]

    # convert the roi to grayscale and blur it
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    contours = ''
    thresh = gray
    # to get the background, keep looking till a threshold is reached
    # so that our running average model gets calibrated
    if num_frames < 20:
        run_avg(gray, aWeight)
    else:
     # segment the hand region
        hand = segment(gray)
        # check whether hand region is segmented
        if hand is not None:
            # if yes, unpack the thresholded image and
            # segmented region
            (thresholded, segmented, tour) = hand
            contours = tour
            thresh = thresholded

            # draw the segmented region and display the frame
            cv2.drawContours(
                clone, [segmented + (right, top)], -1, (0, 0, 255))
            cv2.imshow("Thesholded", thresholded)

    img = thresh
    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img=cv2.imread("240fn.jpg",cv2.IMREAD_GRAYSCALE)
    # img=cv2.cvtColor(bw_image,cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = np.array(img, dtype=np.float32)
    img = np.reshape(img, (1, IMG_SIZE, IMG_SIZE, 1))

    model_out = model.predict([img])[0]
    pred_class = list(model_out).index(max(model_out))
    old_text = text
    if len(contours) > 0:
        contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(contour) > 10000:
            if((max(model_out))*100) > 85:
                text = out_label[pred_class]
            if old_text == text:
                count_same_frame += 1
            else:
                count_same_frame = 0
            if count_same_frame > 50:
                if len(text) == 1:
                    Thread(target=say_text, args=(text, )).start()
                if text == 'space':
                    word += ' '
                elif text == 'del':
                    word = word[:-1]
                else:
                    word = word + text
                count_same_frame = 0
        elif cv2.contourArea(contour) < 1000:
            if word != '':
                # print('yolo')
                # say_text(text)
                Thread(target=say_text, args=(word, )).start()
            text = ""
            word = ""
    else:
        if word != '':
            # print('yolo1')
            # say_text(text)
            Thread(target=say_text, args=(word, )).start()
        text = ""
        word = ""
    blackboard = np.zeros((525, 600, 3), np.uint8)

    cv2.putText(blackboard,
                "Predicted text- " +
                text, (30, 100), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 255, 0))
    # draw the segmented hand
    cv2.rectangle(clone, (left, top), (right, bottom), (0, 255, 0), 2)
    cv2.putText(blackboard, word, (30, 280),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
    if is_voice_on:
        cv2.putText(blackboard, "Voice on", (450, 440),
                    cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 127, 0))
    else:
        cv2.putText(blackboard, "Voice off", (450, 440),
                    cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 127, 0))

    hor = np.hstack((clone, blackboard))
    num_frames += 1
    cv2.imshow("yo", hor)
    keypress = cv2.waitKey(1) & 0xFF

    # if the user pressed "q", then stop looping
    if keypress == ord("q"):
        break
    elif keypress == 27:
        break
    if keypress == ord('v') and is_voice_on:
        is_voice_on = False
    elif keypress == ord('v') and not is_voice_on:
        is_voice_on = True

# free up memory
camera.release()
cv2.destroyAllWindows()
