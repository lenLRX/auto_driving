import cv2
import numpy as np
import sys
import os

# ~/len/data/AutoDriving/Sub/ImageSets/Main/trainval.txt

def compute_avg(img_dir,img_list_txt,_suffix):
    img_list = open(img_list_txt,"r")

    count = 0

    r_sum = 0
    b_sum = 0
    g_sum = 0

    #bgr
    for line in img_list.xreadlines():
        line = line.strip()

        abs_path = os.path.join(img_dir,line)+_suffix

        _img = cv2.imread(abs_path)

        _img_sum = _img.sum(0).sum(0)

        b_sum = b_sum + _img_sum[0]
        g_sum = g_sum + _img_sum[1]
        r_sum = r_sum + _img_sum[2]

        count = count + 1

        if count % 1000 == 0 :
            print "processed: " , count
    
    print "r: ",r_sum/(float(360 * 640 * count)),"g: ",g_sum/(float(360 * 640 * count)),"b: ",b_sum/(float(360 * 640 * count))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "usage: ./compute_avg dir img_list.txt suffix"
        sys.exit()
    compute_avg(sys.argv[1],sys.argv[2],sys.argv[3])