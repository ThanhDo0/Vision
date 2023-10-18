import cv2
import time
import os
import hand as htm #import modul hand
import numpy as np

video = cv2.VideoCapture('http://192.168.1.103:8080/video')

FolderPath="Fingers"
lst=os.listdir(FolderPath)
#print(lst)
lst_2=[]  # khai báo list chứa các mảng giá trị của các hình ảnh/
for i in lst:
    #print(i)
    image=cv2.imread(f"{FolderPath}/{i}")  # Fingers/1.jpg , Fingers/2.jpg ...
    #print(f"{FolderPath}/{i}")
    lst_2.append(image)
# print(len(lst_2))
pTime=0

detector =htm.handDetector(detectionCon=1)
#0.75 độ chính xác 75%

# Khởi tạo các thông tin vật rơi
object_x = np.random.randint(0, 640)  # Vị trí x ngẫu nhiên
object_y = 0  # Vị trí y ban đầu
object_size = 15  # Kích thước đối tượng
object_speed = 10  # Tốc độ rơi của đối tượng

fingerid= [4,8,12,16,20]

while True:
    ret, frame_r = video.read()
    frame = cv2.resize(frame_r, (600,400))
    cv2.imshow("frame", frame)

    hand_frame = detector.findHands(frame)
    lmList = detector.findPosition(hand_frame, draw=False)  # phát hiện vị trí

    if len(lmList) !=0:
        fingers = []
        if lmList[fingerid[0]][1] > lmList[fingerid[-1]][1]:
            hand_side = "Right Hand"
            if lmList[fingerid[0]][1] > lmList[fingerid[0] - 1][1]:
                fingers.append(1)
                # print(lmList[fingerid[0]][1])
                # print(lmList[fingerid[0] - 1][1])
            else:
                fingers.append(0)
            print(lmList)
            # viết cho 4 ngón dài
            for id in range(1, 5):
                if lmList[fingerid[id]][2] < lmList[fingerid[id] - 2][2]:
                    fingers.append(1)
                    print(lmList[fingerid[id]][2])
                    print(lmList[fingerid[id] - 2][2])
                else:
                    fingers.append(0)

            print(fingers)
            songontay = fingers.count(1)
            print(songontay)

            h, w, c = lst_2[songontay - 1].shape
            frame[0:h, 0:w] = lst_2[
                songontay - 1]  # nếu số ngón tay =0 thì lst_2[-1] đẩy về phần tử cuối cùng của list là ảnh 6

            # vẽ thêm hình chữ nhật hiện số ngón tay
            cv2.rectangle(frame, (0, 200), (100, 300), (0, 255, 0), -1)
            cv2.putText(frame, str(songontay), (15, 300), cv2.FONT_HERSHEY_PLAIN, 8, (255, 0, 0), 5)

            #vẽ vật rơi
            if songontay == 1:
                cv2.circle(frame, (object_x, object_y), object_size, (0, 0, 255), -1)

                # Cập nhật vị trí đối tượng rơi
                object_y += object_speed
                if object_y >= frame.shape[0] - 15 - object_size:
                    object_y = 0
                    object_x = np.random.randint(0, 640)
        else:
            hand_side = "Left Hand"
            # viết cho ngón cái (ý tường là điểm 4 ở bên trái hay bên phải điểm 2 )
            if lmList[fingerid[0]][1] < lmList[fingerid[0] - 1][1]:
                fingers.append(1)
                # print(lmList[fingerid[0]][1])
                # print(lmList[fingerid[0] - 1][1])
            else:
                fingers.append(0)
            print(lmList)
            # viết cho 4 ngón dài
            for id in range(1, 5):
                if lmList[fingerid[id]][2] < lmList[fingerid[id] - 2][2]:
                    fingers.append(1)
                    print(lmList[fingerid[id]][2])
                    print(lmList[fingerid[id] - 2][2])
                else:
                    fingers.append(0)

            print(fingers)
            songontay = fingers.count(1)
            print(songontay)

            h, w, c = lst_2[songontay - 1].shape
            frame[0:h, 0:w] = lst_2[
                songontay - 1]  # nếu số ngón tay =0 thì lst_2[-1] đẩy về phần tử cuối cùng của list là ảnh 6

            # vẽ thêm hình chữ nhật hiện số ngón tay
            cv2.rectangle(frame, (0, 200), (100, 300), (0, 255, 0), -1)
            cv2.putText(frame, str(songontay), (15, 300), cv2.FONT_HERSHEY_PLAIN, 8, (255, 0, 0), 5)

            # vẽ vật rơi
            if songontay == 1:
                cv2.circle(frame, (object_x, object_y), object_size, (0, 0, 255), -1)

                # Cập nhật vị trí đối tượng rơi
                object_y += object_speed
                if object_y >= frame.shape[0] - 15 - object_size:
                    object_y = 0
                    object_x = np.random.randint(0, 640)

        # cv2.putText(frame, hand_side, (10, 400), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    cTime=time.time()  # trả về số giây, tính từ 0:0:00 ngày 1/1/1970 theo giờ  utc , gọi là(thời điểm bắt đầu thời gian)
    fps=1/(cTime-pTime) # tính fps Frames per second - đây là  chỉ số khung hình trên mỗi giây
    pTime=cTime
    # show fps lên màn hình, fps hiện đang là kiểu float , ktra print(type(fps))
    cv2.putText(frame, f"FPS: {int(fps)}",(150,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)


    cv2.imshow("Do",frame)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
video.release()
cv2.destroyAllWindows()