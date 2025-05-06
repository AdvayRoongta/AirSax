import streamlit as st
import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

st.title("Saxophone")
uploaded_image = st.camera_input("Take a picture")

note_placeholder = st.empty()
debug_image = st.empty()

def detect_note_from_image(image):
    pressed = []

    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for landmark in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, landmark, mp_hands.HAND_CONNECTIONS)

            if landmark.landmark[8].y > landmark.landmark[6].y:
                pressed.append(1)
            if landmark.landmark[12].y > landmark.landmark[10].y:
                pressed.append(2)
            if landmark.landmark[16].y > landmark.landmark[14].y:
                pressed.append(3)
            if landmark.landmark[4].x < landmark.landmark[3].x:
                pressed.append(9)

        note = ""
        if pressed == [1]:
            note = "b"
        elif pressed == [1, 2]:
            note = "a"
        elif pressed == [2]:
            note = "c"
        elif pressed == [1, 2, 3]:
            note = "g"
        elif pressed == [1, 9]:
            note = "b (High Octave)"
        elif pressed == [1, 2, 9]:
            note = "a (High Octave)"
        elif pressed == [1, 2, 9, 3]:
            note = "g (High Octave)"

        return note if note else "No note", image
    else:
        return "No hand detected", image

if uploaded_image is not None:
    image_bytes = uploaded_image.getvalue()
    file_bytes = np.asarray(bytearray(image_bytes), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)

    note, image_with_landmarks = detect_note_from_image(image)
    note_placeholder.markdown(f"### 🎵 {note}")
    debug_image.image(image_with_landmarks, channels="BGR", caption="Detected landmarks")
