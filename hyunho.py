import cv2
import numpy as np
import pytesseract
import requests
import json

# Mouse Callback함수
def my_crop(event, x,y, flags, param):
    global x1, y1, x2, y2, drawing, finished

    if event == cv2.EVENT_LBUTTONDOWN: #마우스를 누른 상태
        drawing = True
        x1, y1 = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False             # 마우스를 때면 상태 변경
        x2, y2 = x, y

        # 좌표 순서 변경
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        finished = True

drawing = False
finished = False


# 이미지
img = cv2.imread('testt.jpg')


# 이미지 자르기
cv2.namedWindow('image')
cv2.setMouseCallback('image', my_crop)

while True:
	cv2.imshow('image', img)

	k = cv2.waitKey(1) & 0xFF

	if finished == True:        # esc를 누르면 종료
		break

cv2.destroyAllWindows()
img = img[y1:y2, x1:x2]
img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

# 흑백화
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 적응 임계
thr1 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 5)

ihh = cv2.Canny(thr1, 300, 400)
cv2.imshow('ihh', ihh)

_, contours, _ = cv2.findContours(ihh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
img_temp = cv2.drawContours(img, contours, -1, (0,255,0), 1)
cv2.imshow('img_temp', img_temp)

# Opening
kernel1 = np.ones((2, 2), np.uint8)
thr2 = cv2.morphologyEx(thr1, cv2.MORPH_OPEN, kernel1)

# Closing
kernel2 = np.ones((2, 2), np.uint8)
thr3 = cv2.morphologyEx(thr1, cv2.MORPH_CLOSE, kernel2)

# Dilation
kernel3 = np.ones((2, 2), np.uint8)
thr4 = cv2.dilate(thr1, kernel3, iterations=1)

# Erosion
kernel4 = np.ones((2, 2), np.uint8)
thr5 = cv2.erode(thr1, kernel4, iterations=1)


cv2.imshow('gray', gray)
cv2.imshow('thr1', thr1)
cv2.imshow('thr2', thr2)
cv2.imshow('thr3', thr3)
cv2.imshow('thr4', thr4)
cv2.imshow('thr5', thr5)

# 학번 받기
studentID = pytesseract.image_to_string(thr5, config='--psm 6 --oem 2 -c tessedit_char_whitelist=0123456789 tessedit_char_blacklist=QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm!@#$%^&*()_+-=`~,. ')
print(studentID)
studentID = studentID.replace(" ", "")

# 납부 확인
if len(studentID) == 8 and studentID[0:2] == "12":
    URL = "http://www.inhaicesa.com:1666/users/" + studentID + "?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdHVkZW50SWQiOiIxMjE1MTYxNiIsIm5hbWUiOiLsoITsiJjtmIQiLCJwYWlkIjoiMSIsInBob25lIjoiMDEwLTkyNzQtNTg5NyIsImF1dGhMZXZlbCI6NSwiZW1haWxBdXRoIjoxLCJwYXlEYXRlIjpudWxsLCJzY29yZSI6MTAsImlhdCI6MTU0NjI0NzkyOH0.va-yk-cmY-QQYw-W9byq5IOzVCY0GiNv_XZREJG2yTg"
    response = requests.get(URL)
    json_data = json.loads(response.text)
    paid = json_data['payload']['paid']

    if paid == '1':
        print(studentID + ": 납부 했음")
    else:
        print(studentID + ": 납부 안함")
else:
    print("인식 실패")


cv2.waitKey(0)
cv2.destroyAllWindows()
