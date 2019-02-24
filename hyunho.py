# -*- coding: utf-8 -*-

import cv2
import numpy as np
import pytesseract
import requests
import json

# Mouse Callback함수
def draw_circle(event, x,y, flags, param):
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
img = cv2.imread('test4.jpg')

cv2.namedWindow('image')
cv2.setMouseCallback("image", draw_circle)

while True:
	cv2.imshow('image', img)

	k = cv2.waitKey(1) & 0xFF

	if finished == True:        # esc를 누르면 종료
		break

cv2.destroyAllWindows()
img = img[y1:y2, x1:x2]

# 흑백화
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

studentID = pytesseract.image_to_string(gray, config='-psm 7 digits')

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
