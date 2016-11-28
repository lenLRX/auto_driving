import os
import cv2
import numpy as np
import sys

colormap = [[255,0,0],[0,255,0],[0,0,255],[255,255,0],[0,0,0]]


def draw_mboxs(boxfname,pic_dir):
    boxmap = {}
    box_file = open(boxfname,"r")
    for line in box_file.xreadlines():
        lline = line.strip().split(" ")

        fname = lline[0].split("/")[-1].split(".")[0]
        
        if float(lline[2]) < 0.9:
            continue

        box_list = lline[3:]
        box_list.append(lline[1])

        if lline[0] in boxmap:
            boxmap[fname].append(box_list)
        else:
            boxmap[fname] = [box_list]

        #img = cv2.imread(os.path.join(pic_dir,lline[0]) + ".jpg")
    
    for fname in boxmap.keys():
        img = cv2.imread(os.path.join(pic_dir,fname) + ".jpg")
        print os.path.join(pic_dir,fname) + ".jpg"
        for rect in boxmap[fname]:
            cv2.rectangle(img,(int(rect[0]),int(rect[1])),(int(rect[2]),int(rect[3])),colormap[int(rect[4])],3)
            print rect
        cv2.imwrite("F:\\caffe\\detect_result\\" + fname + ".jpg",img)
        #cv2.imshow(fname,img)
    #output label

    lb = np.zeros(img.shape,dtype=np.uint8)

    cv2.rectangle(lb,(0,0),(359,639),[255,0,0],-1)
    cv2.imwrite("F:\\caffe\\detect_result\\Car_label.jpg",lb)

    cv2.rectangle(lb,(0,0),(359,639),[0,255,0],-1)
    cv2.imwrite("F:\\caffe\\detect_result\\Pedestrian_label.jpg",lb)

    cv2.rectangle(lb,(0,0),(359,639),[0,0,255],-1)
    cv2.imwrite("F:\\caffe\\detect_result\\Bicyclist_label.jpg",lb)

    cv2.rectangle(lb,(0,0),(359,639),[255,255,0],-1)
    cv2.imwrite("F:\\caffe\\detect_result\\lights_label.jpg",lb)
    
    cv2.waitKey(-1)
        

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: ./draw_full_result box.txt pic_dir"
        sys.exit()
    draw_mboxs(sys.argv[1],sys.argv[2])