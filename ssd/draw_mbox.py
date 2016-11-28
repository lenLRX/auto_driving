import os
import cv2
import sys


def draw_mboxs(boxfname,pic_dir):
    boxmap = {}
    box_file = open(boxfname,"r")
    for line in box_file.xreadlines():
        lline = line.strip().split(" ")
        
        if float(lline[1]) < 0.999:
            continue

        if lline[0] in boxmap:
            boxmap[lline[0]].append(lline[2:])
        else:
            boxmap[lline[0]] = [lline[2:]]

        #img = cv2.imread(os.path.join(pic_dir,lline[0]) + ".jpg")
    
    for fname in boxmap.keys():
        img = cv2.imread(os.path.join(pic_dir,fname) + ".jpg")
        print os.path.join(pic_dir,fname) + ".jpg"
        for rect in boxmap[fname]:
            cv2.rectangle(img,(int(rect[0]),int(rect[1])),(int(rect[2]),int(rect[3])),(255,0,0),1)
            print rect
        cv2.imwrite("F:\\caffe\\detect_result\\" + fname + ".jpg",img)
        #cv2.imshow(fname,img)
    
    cv2.waitKey(-1)
        

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: ./draw_mbox.py box.txt pic_dir"
        sys.exit()
    draw_mboxs(sys.argv[1],sys.argv[2])