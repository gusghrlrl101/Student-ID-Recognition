import cv2

capture = cv2.VideoCapture(0)  #카메라 받아오기
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  #너비
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)  #높이

while True: #영상 출력 반복
    ret, frame = capture.read()    #프레임 받아오기, ret = 상태 저장, frame = 프레임 저장
    cv2.imshow("VideoFrame",frame) #윈도우 창에 이미지 띄우기
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #cv2.imshow("gray",gray)
    blur = cv2.GaussianBlur(gray,(3,3),0)
    #cv2.imshow("Video",blur)
    #cv2.imwrite('blue.jpg',blur)

    canny=cv2.Canny(blur,100,200)  # edge 인식
    #cv2.imwrite('canny.jpg',canny)
    cv2.imshow("Canny",canny)

    contours,hierarchy = cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        cv2.drawContours(frame,[cnt],-1,(0,255,0),2)
        cv2.imshow('RGB',frame)
        #x,y,w,h = cv2.boundingRect(cnt)
        #rect_area=w*h
        #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)


    if cv2.waitKey(1) > 0 : break  #cv2.waitkey(time) time 마다 키 입력상태 return
                                   #키가 입력될 경우 아스키값 반환

capture.release()  # 메모리 해제
cv2.destroyAllWindows()  # 모든 윈도우창 닫기 cv2.destroyWindow("이름") 가능
