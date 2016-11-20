import cv2
import numpy as np
from matplotlib import pyplot as plt
import random

img = cv2.imread("60_origin.png")
seg = cv2.imread("60_segnet_pred.png")
colorOfCar = [128,0,64]

binary_img = np.zeros((seg.shape[0],seg.shape[1]),dtype="uint8")

for i in xrange(seg.shape[0]):
    for j in xrange(seg.shape[1]):
        if(seg[i][j][0] == colorOfCar[0] and seg[i][j][1] == colorOfCar[1] and seg[i][j][2] == colorOfCar[2]):
            binary_img[i][j] = 255

cv2.imshow("binary_img",binary_img)
cv2.waitKey(-1)

kernel = np.ones((3,3),np.uint8)
#opening = cv2.morphologyEx(binary_img,cv2.MORPH_OPEN,kernel, iterations = 2)
opening = cv2.erode(binary_img,kernel,iterations = 3)

cv2.imshow("opening",opening)
cv2.waitKey(-1)

#sure_bg = cv2.dilate(opening,kernel,iterations=3)
sure_bg = opening
cv2.imshow("sure_bg",sure_bg)
cv2.waitKey(-1)

dist_transform = cv2.distanceTransform(opening,cv2.cv.CV_DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

cv2.imshow("sure_fg",sure_fg)
cv2.waitKey(-1)

sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)

cv2.imshow("unknown",unknown)
cv2.waitKey(-1)

contours,hierarchy = cv2.findContours(sure_bg,cv2.cv.CV_RETR_LIST,cv2.cv.CV_CHAIN_APPROX_SIMPLE)

markers = np.zeros(unknown.shape,dtype=np.int32)

for i in xrange(len(contours)):
    cv2.drawContours(markers,contours,i,i + 1,-1)

cv2.imshow("markers",markers*10000)
cv2.waitKey(-1)

cv2.watershed(img,markers)

print "marker size ", len(contours)

colors =[]

for i in xrange(len(contours)):
    colors.append([random.randint(0,255),random.randint(0,255),random.randint(0,255)])

dst = np.zeros(img.shape,dtype = np.uint8)

for i in xrange(markers.shape[0]):
    for j in xrange(markers.shape[1]):
        idx = markers[i][j]
        #print idx
        if idx > 0 and idx <= len(contours):
            dst[i][j] = colors[idx - 1]
        else:
            dst[i][j] = [0,0,0]
            #print i,j

cv2.imshow("img",img)
cv2.waitKey(-1)

cv2.imshow("dst",dst)
cv2.waitKey(-1)
