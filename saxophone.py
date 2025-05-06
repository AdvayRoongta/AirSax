import streamlit as st
import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2)
st.title("Gesture-Based Note Detector")

uploaded_image = st.camera_input("Take a picture of your hand to detect the note")

note_placeholder = st.empty()

def detect_note_from_image(image):
    pressed = []

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks and results.multi_handedness:
        for landmark, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
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

        note = ""
        if pressed == [1]:
            note = "b"
        elif pressed == [1, 2]:
            note = "a"
        elif pressed == [2]:
            note = "c"
        elif pressed == [1, 2, 3]:
            note = "g"
        elif pressed == [1, 2, 3, 4, 5, 6]:
            note = "d"
        elif pressed == [1, 2, 3, 4]:
            note = "f"
        elif pressed == [1, 2, 3, 4, 5]:
            note = "e"
        elif pressed == [1, 2, 3, 5]:
            note = "f#"
        elif pressed == [1, 9]:
            note = "b (High Octave)"
        elif pressed == [1, 2, 9]:
            note = "a (High Octave)"
        elif pressed == [1, 2, 9, 3]:
            note = "g (High Octave)"

        return note if note else "No note"
    else:
        return "No hand detected"

if uploaded_image is not None:
    image_bytes = uploaded_image.getvalue()
    file_bytes = np.asarray(bytearray(image_bytes), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)

    note = detect_note_from_image(image)
    note_placeholder.markdown(f"### 🎵 {note}")
