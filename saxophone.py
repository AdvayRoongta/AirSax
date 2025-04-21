import cv2
import sys
import mediapipe as mp
#import sounddevice as sd
#import numpy as np 
import simpleaudio as sa
import soundfile as sf
import time
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
hands = mp_hands.Hands(max_num_hands=2)# min_detection_confidence=0.7, min_tracking_confidence=0.7)

pressed=[]
playobj="sigma"
path="sfd"
count=0
def check(note):
    global path
    global playobj
    if path!=(f"{note}.wav"):
        if not isinstance(playobj, str) and playobj.is_playing():
            playobj.stop() #stop
          #  time.sleep(0.25)
    path=f"{note}.wav"
    wave_obj = sa.WaveObject.from_wave_file(path)
    playobj = wave_obj.play()
def ot():
    cv2.putText(image, "Octave", (250, 250), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 230), 2, cv2.LINE_AA)

while True:
    count+=1
    success, image = cap.read() 
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks and results.multi_handedness:
        
        for landmark, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            mp_drawing.draw_landmarks(image,landmark,mp_hands.HAND_CONNECTIONS) #can comment this line
            hand = handedness.classification[0].label 
            if hand.lower()=="left": #a,b,g,c top  also thumb octave key
                if landmark.landmark[8].y > landmark.landmark[6].y:
                            pressed.append(1)
                if landmark.landmark[12].y >landmark.landmark[10].y:
                                                 pressed.append(2)

                if landmark.landmark[16].y >landmark.landmark[14].y:
                                                 pressed.append(3)
                if landmark.landmark[4].x<landmark.landmark[3].x:
                    pressed.append(9)
            if hand.lower()=="right":
                if landmark.landmark[8].y >landmark.landmark[6].y:
                     pressed.append(4)
                if landmark.landmark[12].y >landmark.landmark[10].y:

                    pressed.append(5)

                if landmark.landmark[16].y >landmark.landmark[14].y:
                    pressed.append(6)
         #   if hand.lower()=="left":

        if pressed==[]:
            if not isinstance(playobj, str) and playobj.is_playing():
                            playobj.stop()
        if pressed==[1]:
                cv2.putText(image, "b", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4, cv2.LINE_AA)
                check("b")
        if pressed==[1,2]:
            cv2.putText(image, "a", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4, cv2.LINE_AA) #a
            if path!="":
                if path!="a.wav":
                    if not isinstance(playobj, str) and playobj.is_playing():
                        playobj.stop()
                     #   time.sleep(0.25)
            path="a.wav"
            wave_obj = sa.WaveObject.from_wave_file(path)
            playobj = wave_obj.play()
        if pressed==[2]:
            cv2.putText(image, "c", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4, cv2.LINE_AA)
            if path!="c.wav":
                        if not isinstance(playobj, str) and playobj.is_playing():
                            playobj.stop() #stop
                           # time.sleep(0.25)
            path="c.wav"
            wave_obj = sa.WaveObject.from_wave_file(path)
            playobj = wave_obj.play()
        if pressed==[1,2,3]:
            cv2.putText(image, "g", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4, cv2.LINE_AA)

            check("g")
        if pressed==[1,2,3,4,5,6]:
            cv2.putText(image, "d", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4, cv2.LINE_AA)          #  d, s = sf.read("d.wav")
            check("d")
        if pressed==[1,2,3,4]:
            cv2.putText(image, "f", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4, cv2.LINE_AA)
            check("f")
        if pressed==[1,2,3,4,5]:
            cv2.putText(image, "e", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4, cv2.LINE_AA)
            check("e")
        if pressed==[1,2,3,5]:
            cv2.putText(image, "f#", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4, cv2.LINE_AA)
            check("fsharp")

#HIGH

        if pressed==[1,9]:
                cv2.putText(image, "b", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4, cv2.LINE_AA)
                check("highb")
                ot()
        if pressed==[1,2,9]:
            cv2.putText(image, "a", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4, cv2.LINE_AA) #a
            check("higha")
            ot()
        if pressed==[2,9]:
            cv2.putText(image, "c", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4, cv2.LINE_AA)
            ot()
            if path!="highc.wav":
                        if not isinstance(playobj, str):
                            playobj.stop() #stop
                            time.sleep(0.25)
            path="highc.wav"
            wave_obj = sa.WaveObject.from_wave_file(path)
            playobj = wave_obj.play()
        if pressed==[1,2,3,9]:
            cv2.putText(image, "g", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4, cv2.LINE_AA) 
            check("highg")
            ot()
        if pressed==[1,2,3,9,4,5,6]:
            cv2.putText(image, "d", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4, cv2.LINE_AA)          #  d, s = sf.read("d.wav")
            check("highd")
            ot()
        if pressed==[1,2,3,4,9]:
            cv2.putText(image, "f", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4, cv2.LINE_AA)
            check("highf")
            ot()
        if pressed==[1,2,3,4,5,9]:
            cv2.putText(image, "e", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4, cv2.LINE_AA)
            check("highe")
            ot()
        if pressed==[1,2,3,5,9]:
            ot()
            cv2.putText(image, "f#", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4, cv2.LINE_AA)
            check("highfsharp")
        
        pressed=[]

        
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        sys.exit()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
