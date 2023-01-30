import numpy as np
import cv2
import time
import os
import imutils

my_track_method = cv2.legacy.TrackerCSRT_create()
cap = cv2.VideoCapture(0)
print('EXPOSURE',cap.get(cv2.CAP_PROP_EXPOSURE))
cap.set(cv2.CAP_PROP_EXPOSURE, -15) 
print('CAP_PROP_BRIGHTNESS',cap.get(cv2.CAP_PROP_BRIGHTNESS))
cap.set(cv2.CAP_PROP_BRIGHTNESS, -60)
print('Staturation',cap.get(cv2.CAP_PROP_SATURATION))
cap.set(cv2.CAP_PROP_SATURATION,40)
print('Constrast: ',cap.get(cv2.CAP_PROP_CONTRAST))
cap.set(cv2.CAP_PROP_CONTRAST, -10 )
#print('CAP_PROP_BRIGHTNESS',cap.get(cv2.CAP_PROP_BRIGHTNESS))

# Biến đếm, để chỉ lưu dữ liệu sau khoảng 60 frame, tránh lúc đầu chưa kịp cầm tiền lên
i=0
while(True):
    # Capture frame-by-frame
    #
    i+=1
    ret, frame = cap.read()
    if not ret:
        continue
    #frame = cv2.resize(frame, dsize=None,fx=0.3,fy=0.3)
    if i<10:
        continue
    if i==10:
        cv2.imwrite("linh.png",frame)
        select_box = cv2.selectROI(frame)
        select_box1 = select_box 
        print('selec_box: ', type(select_box[0]))
        my_track_method.init(frame, select_box)
    # Hiển thị
    ret, select_box = my_track_method.update(frame)
    if ret:
        tl, br  = (int(select_box[0]), int(select_box[1])), (int(select_box[0] + select_box[2]), int(select_box[1] + select_box[3]))
        cv2.rectangle(frame, tl, br, (0, 255, 0), 2, 2)
        select_box = (int(select_box[0]), int(select_box[1]), int(select_box[2]), int(select_box[3]))

        #print('selec_box2222: ', select_box)
        img= frame[select_box[1]:select_box[1]+select_box[3],select_box[0]:select_box[0]+select_box[2]]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thres = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,9,-30)
        thres1=cv2.resize(thres,(img.shape[1]*4,img.shape[0]*4))
        #cv2.imshow('Thres',thres1)
        contours = cv2.findContours(thres, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv2.contourArea, reverse=False)
        #print('Contours',contours)
        number = 0
        ma =[[],[],[],[]]
        td =[] 
        for c in contours:
            (x, y, w, h) = cv2.boundingRect(c)
            # print(x, y, w, h)
            #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # approximate the contour
            if (3<w<20) and(3<h<20):
                ma[0].append(x)
                ma[1].append(y)
                a =[x+w/2,y+h/2] #Tin toa do tam cua các box LED
                td.append(a)
                ma[2].append(w)
                ma[3].append(h)
                #if x==min(maX)and y==min(maY):
                #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
                #print(x, y, w, h)
                number +=1
        #print('Xmin: ',ma)
        #Roi LED cạnh
        # print('Td==',td)
        xmin = min(ma[0])
        # print('xmin==',xmin)
        # print('X',ma[0])
        xmax = max(ma[0])
        # print('xmax==',xmax)
        ymin = min(ma[1])
        ymax = max(ma[1])
        
        # Xu ly bit==========================================
        bit=[]
        dx = (xmax-xmin)/(8-1)
        # print('dx=',dx)
        dy = (ymax-ymin)/(8-1)
        # print('dy=',dy)
        c = ymin
        while c <= ymax+1: 
            # print('x=====',c)
            b = xmin
            while b <= xmax+1:
                for j in td:
                    if b <= j[0] <= b+dx and c <= j[1] <= c+dy:
                        d=1
                        break
                    else:
                        d=0
                bit.append(d)


                # print('y=======',b)----+++++++++++++++++++
                b = b+dx
            c +=dy

       # print(len(bit),'==>',bit)
        print("Number of Contours found = " + str(number))
        img1=cv2.resize(img,(img.shape[0]*4,img.shape[1]*4))
        #cv2.imshow('Pix',img1)
           # my_track_method.init(frame, select_box)
        
    # Tính và hiển thị nhiệt độ và độ ẩm
        tem = bit[8:16]
        tem1 = sum(val*(2**idx) for idx, val in enumerate(reversed(tem)))
        if bit[0:8]==[1,0,1,1,1,0,0,1]:
            cv2.putText(frame, "Text Print: " + chr(tem1) +".....", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('frame',frame)
    else:
        cv2.putText(frame, "Object can not be tracked!", (80, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow('frame',frame)
       # continue
    
    # Lưu dữ liệu
    if i==60:
        print("Số ảnh capture = ",i-60)

    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break
    if cv2.waitKey(1) & 0xFF == ord('r'):
        select_box =cv2.selectROI(frame)
        my_track_method.clear()
        my_track_method = cv2.legacy.TrackerCSRT_create()
        my_track_method.init(frame,select_box)
        #continue

# When everything done, release the capture

#refrensi 
#https://www.adamsmith.haus/python/answers/how-to-convert-an-int-to-ascii-and-back-in-python
