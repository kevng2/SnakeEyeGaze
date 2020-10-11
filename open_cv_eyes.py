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
    # horizontal_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
    # vertical_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)

    horizontal_line_length = hypot(left_point[0] - right_point[0], left_point[1] - right_point[1])
    vertical_line_length = hypot(center_top[0] - center_bottom[0], center_top[1] - center_bottom[1])

    ratio = horizontal_line_length // vertical_line_length
    return ratio


def division(n, d):
    return n / d if d else 0


def get_gaze_ratio(eye_points, facial_landmarks):
    left_eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                                (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                                (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                                (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                                (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                                (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)
                                ], np.int32)

    height, width, _ = frame.shape
    mask = np.zeros((height, width), np.uint8)

    # fill the eye area with white
    cv2.polylines(mask, [left_eye_region], True, 225, 2)
    cv2.fillPoly(mask, [left_eye_region], 255)

    eye = cv2.bitwise_and(gray, gray, mask=mask)

    # draws circle around eye
    # cv2.polylines(frame, [left_eye_region], True, (0, 0, 225), 2)

    # smallest x value (left point on eye)
    min_x = np.min(left_eye_region[:, 0])

    # biggest x value (right point on eye)
    max_x = np.max(left_eye_region[:, 0])

    # smallest y value (bottom of eye)
    min_y = np.min(left_eye_region[:, 1])

    # biggest y value (top of eye)
    max_y = np.max(left_eye_region[:, 1])

    # get the eye area from the the bottom point to the top point and leftmost point to rightmost point
    gray_eye = eye[min_y:max_y, min_x:max_x]

    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
    height, width = threshold_eye.shape
    left_side_threshold = threshold_eye[0: height, 0: width // 2]
    left_side_white = cv2.countNonZero(left_side_threshold)

    bottom_side_threshold = threshold_eye[0: height // 2, 0: width]
    bottom_side_white = cv2.countNonZero(bottom_side_threshold)

    top_side_threshold = threshold_eye[height // 2: height, 0: width]
    top_side_white = cv2.countNonZero(top_side_threshold)

    right_side_threshold = threshold_eye[0: height, width // 2: width]
    right_side_white = cv2.countNonZero(right_side_threshold)

    ratio = division(left_side_white, right_side_white)
    verticalRatio = division(top_side_white, bottom_side_white)

    return ratio, verticalRatio


if __name__ == '__main__':

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

            gaze_ratio_left_eye, gaze_ratio_left_eye_vertical = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks)
            gaze_ratio_right_eye, gaze_ratio_right_eye_vertical = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)

            gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2
            gaze_ratio_vertical = (gaze_ratio_left_eye_vertical + gaze_ratio_right_eye_vertical) // 2

            cv2.putText(frame, str(gaze_ratio_vertical), (100, 50), font, 2, (0, 0, 255), 3)

            # gaze detection
            if gaze_ratio < 1:
                cv2.putText(frame, "RIGHT", (50, 100), font, 2, (0, 0, 255), 3)
            elif 1 < gaze_ratio < 3:
                # check vertical here
                if gaze_ratio_vertical > 2:
                    cv2.putText(frame, "UP", (50, 100), font, 2, (0, 0, 255), 3)
                else:
                    cv2.putText(frame, "DOWN", (50, 100), font, 2, (0, 0, 255), 3)

                pass
            else:
                cv2.putText(frame, "LEFT", (50, 100), font, 2, (0, 0, 255), 3)

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
