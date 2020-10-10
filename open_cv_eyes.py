import cv2
import numpy as np
import dlib
from math import hypot


def midpoint(p1, p2):
    return (p1.x + p2.x) // 2, (p1.y + p2.y) // 2


def get_blinking_ratio(eye_points, facial_landmarks):
    # points on the eye
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    # lines to draw across the eye
    horizontal_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
    vertical_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)

    horizontal_line_length = hypot(left_point[0] - right_point[0], left_point[1] - right_point[1])
    vertical_line_length = hypot(center_top[0] - center_bottom[0], center_top[1] - center_bottom[1])

    ratio = horizontal_line_length // vertical_line_length
    return ratio


# change number to 0 for default webcam on your machine
cap = cv2.VideoCapture(1)

# set resolution to 640x480
cap.set(3, 640)
cap.set(4, 480)

# face detector
detector = dlib.get_frontal_face_detector()

# read file to get the face data
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

font = cv2.FONT_HERSHEY_PLAIN

while True:
    # get the frame data from the capture
    _, frame = cap.read()

    # used to improve performance
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)

        # Detect Blinking
        left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
        right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
        blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2
        if blinking_ratio > 5.0:
            cv2.putText(frame, "BLINKING", (50, 150), font, 7, (255, 0, 0))

        # Gaze Detection
        left_eye_region = np.array([(landmarks.part(36).x, landmarks.part(36).y),
                                    (landmarks.part(37).x, landmarks.part(37).y),
                                    (landmarks.part(38).x, landmarks.part(38).y),
                                    (landmarks.part(39).x, landmarks.part(39).y),
                                    (landmarks.part(40).x, landmarks.part(40).y),
                                    (landmarks.part(41).x, landmarks.part(41).y)
                                    ], np.int32)

        # draws circle around eye
        cv2.polylines(frame, [left_eye_region], True, (0, 0, 225), 2)
        cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
