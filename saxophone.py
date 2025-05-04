import sys
import os
import streamlit as st
import cv2
import mediapipe as mp
import simpleaudio as sa
import time

sys.stdout = open(os.devnull, 'w')
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
hands = mp_hands.Hands(max_num_hands=2)

pressed = []
playobj = "sigma"
path = "sfd"
count = 0
def check(note):
    global path
    global playobj
    if path != (f"{note}.wav"):
        if not isinstance(playobj, str) and playobj.is_playing():
            playobj.stop()  # stop
    path = f"{note}.wav"
    wave_obj = sa.WaveObject.from_wave_file(path)
    playobj = wave_obj.play()

def ot():
    return "Octave"

st.title("Hand Gesture Music Player")
st.write("Use hand gestures to play different notes.")
while True:
    success, image = cap.read()
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks and results.multi_handedness:
        for landmark, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            mp_drawing.draw_landmarks(image, landmark, mp_hands.HAND_CONNECTIONS)
            hand = handedness.classification[0].label

            if hand.lower() == "left":
                if landmark.landmark[8].y > landmark.landmark[6].y:
                    pressed.append(1)
                if landmark.landmark[12].y > landmark.landmark[10].y:
                    pressed.append(2)
                if landmark.landmark[16].y > landmark.landmark[14].y:
                    pressed.append(3)
                if landmark.landmark[4].x < landmark.landmark[3].x:
                    pressed.append(9)
            if hand.lower() == "right":
                if landmark.landmark[8].y > landmark.landmark[6].y:
                    pressed.append(4)
                if landmark.landmark[12].y > landmark.landmark[10].y:
                    pressed.append(5)
                if landmark.landmark[16].y > landmark.landmark[14].y:
                    pressed.append(6)

        if pressed == []:
            if not isinstance(playobj, str) and playobj.is_playing():
                playobj.stop()

        if pressed == [1]:
            st.text("b")
            check("b")
        elif pressed == [1, 2]:
            st.text("a")
            check("a")
        elif pressed == [2]:
            st.text("c")
            check("c")
        elif pressed == [1, 2, 3]:
            st.text("g")
            check("g")
        elif pressed == [1, 2, 3, 4, 5, 6]:
            st.text("d")
            check("d")
        elif pressed == [1, 2, 3, 4]:
            st.text("f")
            check("f")
        elif pressed == [1, 2, 3, 4, 5]:
            st.text("e")
            check("e")
        elif pressed == [1, 2, 3, 5]:
            st.text("f#")
            check("fsharp")

        if pressed == [1, 9]:
            st.text("b (High Octave)")
            check("highb")
            st.text(ot())
        if pressed == [1, 2, 9]:
            st.text("a (High Octave)")
            check("higha")
            st.text(ot())

        pressed = []
    st.image(image, channels="BGR", use_column_width=True)
    sys.stdout = sys.__stdout__
