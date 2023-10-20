import cv2
import time
import mediapipe as mp

cap = cv2.VideoCapture('http://192.168.1.103:8080/video')

mpHands = mp.solutions.hands
hands = mpHands.Hands(False)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    ret, frame_full = cap.read()
    frame = cv2.resize(frame_full, (600, 400))

    if not ret:
        break

    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    print(str(results.multi_hand_landmarks))
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id,lm)
                h, w, c = frame.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                # print(id, cx, cy)
                if id == 4:
                    cv2.circle(frame, (cx, cy), 5, (255,0,0),cv2.FILLED)

            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(frame,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0))


    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên và đóng cửa sổ
cap.release()
cv2.destroyAllWindows()