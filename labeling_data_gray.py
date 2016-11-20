import cv2
import numpy as np
import os
import json
import sys

color_table = {
1:0,
2:1,
3:2,
20:3,
}



def convert2gray_label(label_dir,train_dir):
    label_file = os.path.join(train_dir,'label.idl')
    label_json = None
    json_file = open(label_file,"r")

    for line in json_file.readlines():
        line = line.strip()
        label_json = json.loads(line)
        for fname in label_json:
            rect_list = label_json[fname]
            _img = cv2.imread(os.path.join(train_dir,fname))
            
            _gray = np.zeros(_img.shape,dtype="uint8")
            _gray.fill(4)
            for rect in rect_list:
                print rect
                cv2.rectangle(_gray,(int(rect[0]),int(rect[1])),(int(rect[2]),int(rect[3])),color_table[rect[4]],-1)
            
            cv2.imwrite(os.path.join(label_dir,fname.split(".")[0] + ".png"),_gray)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: labeling_data_gray data_dir label_dir"
        exit(0)
    convert2gray_label(sys.argv[1],sys.argv[2])