import xml.etree.cElementTree as ET
import os
import json
import sys
import cv2
import numpy as np

name_table = {
1:"car",
2:"person",
3:"Bicyclist",
20:"lights",
}


def json2xml(train_dir,label_dir):
    label_file = os.path.join(train_dir,'label.idl')
    label_json = None
    json_file = open(label_file,"r")

    for line in json_file.readlines():
        line = line.strip()
        label_json = json.loads(line)
        for fname in label_json:
            rect_list = label_json[fname]
            _img = cv2.imread(os.path.join(train_dir,fname))
            annot = ET.Element("annotation")
            folder = ET.SubElement(annot,"folder")
            folder.text = "training"
            filename = ET.SubElement(annot,"filename")
            filename.text = fname
            xml_size = ET.SubElement(annot,"size")
            ET.SubElement(xml_size,"width").text = str(_img.shape[1])
            ET.SubElement(xml_size,"height").text = str(_img.shape[0])
            ET.SubElement(xml_size,"depth").text = str(_img.shape[2])
            segmented = ET.SubElement(annot,"segmented")
            segmented.text = "0"

            for rect in rect_list:
                _Object = ET.SubElement(annot,"object")
                _name = ET.SubElement(_Object,"name")
                _name.text = name_table[rect[4]]
                _difficult = ET.SubElement(_Object,"difficult")
                _bndbox = ET.SubElement(_Object,"bndbox")
                ET.SubElement(_bndbox,"xmin").text = str(int(rect[0]))
                ET.SubElement(_bndbox,"ymin").text = str(int(rect[1]))
                ET.SubElement(_bndbox,"xmax").text = str(int(rect[2]))
                ET.SubElement(_bndbox,"ymax").text = str(int(rect[3]))
            
            tree = ET.ElementTree(annot)
            tree.write(os.path.join(label_dir,fname.split(".")[0] + ".xml"))



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: labeling_data_gray data_dir label_dir"
        exit(0)
    json2xml(sys.argv[1],sys.argv[2])