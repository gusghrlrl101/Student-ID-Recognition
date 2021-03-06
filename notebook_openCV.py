import cv2

capture = cv2.VideoCapture(0)  #카메라 받아오기
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  #너비
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)  #높이

#ret, frame = capture.read()    #프레임 받아오기, ret = 상태 저장, frame = 프레임 저장
frame = cv2.imread('test1.jpg')
#cv2.imshow("VideoFrame",frame) #윈도우 창에 이미지 띄우기
gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#cv2.imshow("gray",gray)
blur = cv2.GaussianBlur(gray,(3,3),0)
#cv2.imshow("Video",blur)
#cv2.imwrite('blue.jpg',blur)

canny=cv2.Canny(blur,80,100)  # edge 인식
cv2.imwrite('canny.jpg',canny)
cv2.imshow("Canny",canny)

contours,hierarchy = cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
minx=15000
miny=15000
maxx=0
maxy=0
for cnt in contours:
    area = cv2.contourArea(cnt)
    x,y,w,h = cv2.boundingRect(cnt)
    rect_area = w*h
    if(rect_area>=10000):
        #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
        if(minx > x):minx=x
        if(miny > y):miny=y
        if(maxx < x+w):maxx=x+w
        if(maxy < y+h):maxy=y+h
        #cv2.drawContours(frame,[cnt],-1,(0,255,0),2)
        #x,y,w,h = cv2.boundingRect(cnt)
        #rect_area=w*h
        #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)

#cv2.circle(frame,(maxx,maxy),1,(0,0,255),5) #red
#cv2.circle(frame,(minx,miny),1,(255,0,0),5) #blue
cv2.imshow('RGB',frame)
trim = frame[miny:maxy,minx:maxx]
cv2.imwrite('trim.jpg',trim)
cv2.circle(trim,(220,190),1,(255,0,0),5) #blue
cv2.circle(trim,(250,420),1,(0,0,255),5) #red
cv2.rectangle(trim,(250,420),(220,190),(0,255,0),1)
img = cv2.imshow('trim',trim)

while (1):
    if cv2.waitKey(1) > 0 : break

capture.release()  # 메모리 해제
cv2.destroyAllWindows()  # 모든 윈도우창 닫기 cv2.destroyWindow("이름") 가능
