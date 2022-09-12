import math

import mediapipe as mp
import cv2
import time
from collections import deque

import numpy as np

# desenha ou nao os pontos da mao
draw_hands = True
#draw_hands = False

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0
fpss = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
fpsMean = deque(fpss)

def calculate_joints_distances(point1, point2):
    return math.sqrt(((point2[0] - point1[0]) * (point2[0] - point1[0])) + ((point2[1] - point1[1]) * (point2[1] - point1[1])))

def desenha_linha(points):
    cv2.polylines(img, [np.array(points, np.int32)], False, (0, 255, 255), 5)
    pointsAdded = []
    for item in points:
        pointsAdded.append([x + 3 for x in item])
    cv2.polylines(img, [np.array(pointsAdded, np.int32)], False, (0, 255, 0), 5)

list_of_points = []
linhas_desenhadas = []

while True:
    list_hand_joints = []
    success, img = cap.read()

    cv2.flip(img,1,img)

    results = hands.process(img)

    ponto1 = None
    ponto2 = None
    ponto3 = None

    if results.multi_hand_landmarks:
        cv2.putText(img, "o", (10, 10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 3)
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if draw_hands:
                    #draw hand numbers
                    cv2.putText(img, str(id),(cx,cy), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 3)
                list_hand_joints.append((cx, cy))
                if id == 4:
                    point3 = (cx, cy)
                    pointPoly = [cx, cy]

            # draw hands connections
            if draw_hands:
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    if not list_hand_joints == []:
        drawingDistance = calculate_joints_distances(list_hand_joints[8], list_hand_joints[4])
        apagar = calculate_joints_distances(list_hand_joints[20], list_hand_joints[4])
        print_distance = True
        if print_distance:
            cv2.putText(img, str(int(drawingDistance)), (200, 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 3)
        if drawingDistance < 60:
            list_of_points.append(pointPoly)
            cv2.circle(img, point3, 5, (255, 255, 255), -1)
        else:
            if not list_of_points == []:
                if len(list_of_points) >= 3:
                    linhas_desenhadas.append(list_of_points)
                list_of_points = []


        # clear all points
        if apagar > 180:
            linhas_desenhadas = []
            list_of_points = []

    if len(list_of_points) >= 3:
        desenha_linha(list_of_points)
    for linha in linhas_desenhadas:
        desenha_linha(linha)

    calculate_fps = False
    if calculate_fps:
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        fpsMean.popleft()
        fpsMean.append(fps)

        # prints FPS
        cv2.putText(img, str(int(sum(fpsMean) / len(fpsMean))), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Inteligencia Mil Grau = IMG", img)
    k = cv2.waitKey(1)
    if k == ord("q"):
        break

cv2.destroyAllWindows()
cap.release()
print("Encerrou corretamente")
