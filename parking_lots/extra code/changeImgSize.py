import numpy as np;
import cv2;

for i in range(201, 207):
    img = cv2.imread("/Users/hanyuchen/Desktop/img2/" + str(i) + ".png",1)
    cutimg = img[16:,16:2010]
    cv2.imwrite("/Users/hanyuchen/Desktop/img2/" + str(i) + ".jpg",cutimg)
