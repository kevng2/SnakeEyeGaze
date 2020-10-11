import cv2
import numpy as np
import dlib
from math import hypot
import pygame
import sys
import random


class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [((screen_width / 2), (screen_height / 2))]
        self.direction = (0, 0)
        self.color = (255, 0, 0)
        # Special thanks to YouTubers Mini - Cafetos and Knivens Beast for raising this issue!
        # Code adjustment courtesy of YouTuber Elija de Hoog
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self, surface):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * gridsize)) % screen_width), (cur[1] + (y * gridsize)) % screen_height)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        elif self.positions[0][0] == 0.0 and x == -1:
            self.reset()
        elif self.positions[0][0] == 460.0 and x == 1:
            self.reset()
        elif self.positions[0][1] == 0.0 and y == -1:
            self.reset()
        elif self.positions[0][1] == 460.0 and y == 1:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((screen_width / 2), (screen_height / 2))]
        self.direction = (0, 0)
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((int(p[0]), int(p[1])), (gridsize, gridsize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (0, 0, 0), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if direction == "UP":
                self.turn(up)
            elif direction == "DOWN":
                self.turn(down)
            elif direction == "LEFT":
                self.turn(left)
            elif direction == "RIGHT":
                self.turn(right)


class Food():
    def __init__(self):
        self.position = (0, 0)
        self.color = (223, 163, 49)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, grid_width - 1) * gridsize, random.randint(0, grid_height - 1) * gridsize)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (223, 163, 49), r, 1)


def drawGrid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x + y) % 2 == 0:
                r = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, (255, 255, 255), r)
            else:
                rr = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, (255, 255, 255), rr)


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


screen_width = 480
screen_height = 480

gridsize = 20
grid_width = screen_width / gridsize
grid_height = screen_height / gridsize

up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

surface = pygame.Surface(screen.get_size())
surface = surface.convert()
drawGrid(surface)

snake = Snake()
food = Food()

myfont = pygame.font.SysFont("monospace", 16)

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

    direction = "DOWN"

    while True:
        clock.tick(1)
        drawGrid(surface)
        snake.move(surface)
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        text = myfont.render("Score {0}".format(snake.score), 1, (0, 0, 0))
        screen.blit(text, (5, 10))
        pygame.display.update()

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
                direction = "RIGHT"
                snake.handle_keys()

            elif 1 < gaze_ratio < 3:
                # check vertical here
                if gaze_ratio_vertical > 2:
                    cv2.putText(frame, "UP", (50, 100), font, 2, (0, 0, 255), 3)
                    direction = "UP"
                    snake.handle_keys()

                else:
                    cv2.putText(frame, "DOWN", (50, 100), font, 2, (0, 0, 255), 3)
                    direction = "DOWN"
                    snake.handle_keys()
            else:
                direction = "LEFT"
                cv2.putText(frame, "LEFT", (50, 100), font, 2, (0, 0, 255), 3)
                snake.handle_keys()

        cv2.imshow("Pupil Recognition", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
