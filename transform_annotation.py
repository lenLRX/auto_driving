from PIL import Image
import os
import sys

transform_table = {
    0:4,
    1:4,
    2:4,
    3:4,
    4:4,
    5:4,
    6:4,
    7:4,
    8:0,
    9:1,
    10:2,
    11:4,
}

def transform(thepath):
    files = os.listdir(thepath)
    for f in files:
        if f.endswith(".png"):
            fpath = os.path.join(thepath,f)
            origin = Image.open(fpath)
            size = origin.size
            img = Image.new("L",size)
            
            for i in xrange(size[0]):
                for j in xrange(size[1]):
                    pix = origin.getpixel((i,j))
                    img.putpixel((i,j),transform_table[pix])
            
            img.save(fpath)

if __name__ == "__main__":
    if len(sys.argv) !=2 :
        print "usage: ./transform_annotation.py path"
        sys.exit(0)
    transform(sys.argv[1])