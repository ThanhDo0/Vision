import cv2
import numpy as np

# Đọc hình ảnh chứa đối tượng cần nhận diện
path1 = r'D:\Work\Learning\Picture\anh1.jpg'
path2 = r'D:\Work\Learning\Picture\anh1cut.jpg'
s_img = cv2.imread(path1)
s_img = cv2.cvtColor(s_img, cv2.COLOR_BGR2RGB)
t_img = cv2.imread(path2)
t_img = cv2.cvtColor(t_img, cv2.COLOR_BGR2RGB)

method = eval('cv2.TM_CCOEFF')
s_img_copy = s_img.copy()
# Lấy chiều rộng và chiều cao của template
# w, h = template.shape[::-1]
# Thực hiện Template Matching
res = cv2.matchTemplate(s_img_copy, t_img, method)
# Lấy vị trí tối ưu của kết quả tương tự
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
if method in [cv2.TM_SQDIFF_NORMED, cv2.TM_SQDIFF]:
    top_left = min_loc
else:
    top_left = max_loc
heigh, width, channel = t_img.shape
bottom_right = (top_left[0] + width, top_left[1] + heigh)
# Vẽ hình chữ nhật xung quanh đối tượng trùng khớp
cv2.rectangle(s_img, top_left, bottom_right, (255, 0, 0), 1)

# Hiển thị kết quả
cv2.imshow('Matching Result', s_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
