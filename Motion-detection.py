import cv2
import numpy as np

# Khởi tạo webcam
cap = cv2.VideoCapture('http://192.168.1.103:8080/video')

# Đọc một khung hình đầu tiên để so sánh
ret, frame_pr = cap.read()
prev_frame = cv2.resize(frame_pr, (600, 400))

while True:
    # Đọc khung hình hiện tại
    ret, frame = cap.read()
    current_frame = cv2.resize(frame, (600, 400))
    
    if not ret:
        break

    # Chuyển đổi khung hình sang ảnh xám
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

    # Tính toán chênh lệch giữa hai khung hình xám
    frame_diff = cv2.absdiff(prev_gray, current_gray)

    # Áp dụng ngưỡng để nhận biết vùng chuyển động
    _, thresholded_diff = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)

    # Tìm các đường viền trong vùng chuyển động
    contours, _ = cv2.findContours(thresholded_diff.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Vẽ hình chữ nhật bao quanh các đường viền
    for contour in contours:
        if cv2.contourArea(contour) > 1000:  # Lọc các đường viền nhỏ
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(current_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Hiển thị khung hình với vùng di chuyển bắt được
    cv2.imshow('Finger Movement Detection', current_frame)

    # Cập nhật khung hình trước để sử dụng trong lần lặp tiếp theo
    prev_frame = current_frame

    # Điều khiển bằng phím 'q', thoát vòng lặp
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
