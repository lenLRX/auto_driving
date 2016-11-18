import cv2
import os
import json

color_table = {
1:[64,0,128],
2:[64,64,0],
3:[0,129,192],
20:[64,64,128],
}

label_dir = '../training_label/'
train_dir = '../training/'
label_file = os.path.join(train_dir,'label.idl')
label_json = None
json_file = open(label_file,"r")

for line in json_file.readlines():
    line = line.strip()
    label_json = json.loads(line)
    for fname in label_json:
        rect_list = label_json[fname]
        _img = cv2.imread(os.path.join(train_dir,fname))
        for rect in rect_list:
            cv2.rectangle(_img,(int(rect[0]),int(rect[1])),(int(rect[2]),int(rect[3])),color_table[rect[4]],-1)
        
        cv2.imwrite(os.path.join(train_dir,fname.split(".")[0] + ".png"),_img)