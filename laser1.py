import cv2
import numpy as np

cap=cv2.VideoCapture("D:\\Desktop\\laser2.mp4")

def nothing(a):
    pass


cv2.namedWindow('controls', 2)
# create trackbar in 'controls' window with name 'r''
cv2.createTrackbar('r', 'controls', 0, 255, nothing)
cv2.createTrackbar('g', 'controls', 0, 255, nothing)
cv2.createTrackbar('b', 'controls', 0, 255, nothing)
cv2.createTrackbar('h', 'controls', 0, 255, nothing)
cv2.createTrackbar('s', 'controls', 0, 255, nothing)
cv2.createTrackbar('v', 'controls', 0, 255, nothing)

def getContours(edged, imgContour,areas,xcor1,ycor1):
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        areas.append(area)
        if area < 640 * 480:
            peri = cv2.arcLength(cnt, True)  # konturun çevresini hesaplar.
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, closed=True)
            cv2.drawContours(imgContour, [approx], -1, (0, 0, 255), 1)
            M = cv2.moments((cnt))

            distx=0
            disty=0
            if (M["m10"]!=0):

                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                #print("x koordinatı:")
                #print(cX)
                xcor.append(cX)
                #print("y koordinatı")
                #print(cY)
                ycor.append(cY)

                if len(xcor) == 2:
                        distx=xcor[1]-xcor[0]
                        cv2.putText(imgContour, 'x mesafe=', (0, cY - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)
                        cv2.putText(imgContour, str(distx), (0,cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (255, 255, 255), 2)

                if len(ycor) == 2:
                    disty = ycor[1] - ycor[0]
                    cv2.putText(imgContour, 'y mesafe=', (0, cY -10 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (255, 255, 255), 2)
                    cv2.putText(imgContour, str(disty), (0, cY +3), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (255, 255, 255), 2)


                cv2.putText(imgContour, str(cX), (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 255, 255), 2)
                cv2.putText(imgContour, str(cY), (cX - 10, cY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 255, 255), 2)

                cv2.circle(imgContour, (cX, cY), 7, (255, 255, 255), -1)




while True:
    ret,frame=cap.read()
    font = cv2.FONT_HERSHEY_PLAIN
    frame = cv2.flip(frame, 1)
    if ret:
        b, g, r = cv2.split(frame)
        r = r * cv2.getTrackbarPos('r', 'controls')
        g = g * cv2.getTrackbarPos('g', 'controls')
        b = b * cv2.getTrackbarPos('b', 'controls')
        merged = cv2.merge([r, g, b])
        cv2.imshow("merge", merged)
        hsv = cv2.cvtColor(merged, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        h = h + cv2.getTrackbarPos('h', 'controls')
        s = s + cv2.getTrackbarPos('s', 'controls')
        v = v + cv2.getTrackbarPos('v', 'controls')
        final_hsv = cv2.merge((h, s, v))

        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        cv2.imshow("img", img)

        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        blurred = cv2.medianBlur(gray, 9)
        edged = cv2.Canny(gray, 30, 200)
        cv2.imshow("edged",edged)
        cv2.imshow("frame",frame)
        imgContour = frame.copy()
        areas=[]
        xcor = []
        ycor = []
        getContours(edged, imgContour,areas,xcor,ycor)
        cv2.imshow("imgContour", imgContour)

    else:
        cap=cv2.VideoCapture("D:\\Desktop\\laser2.mp4")

    if cv2.waitKey(1)&0xFF == ord('q'):
        break