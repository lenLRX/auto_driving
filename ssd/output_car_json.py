import sys
import json

def output_car_json(car_out,out_json):
    boxmap = {}
    box_file = open(car_out,"r")
    for line in box_file.xreadlines():
        lline = line.strip().split(" ")
        if float(lline[1]) < 0.999:
            continue
        data_l = [float(lline[2]),float(lline[3]),float(lline[4]),float(lline[5]),1,float(lline[1])]
        fname = lline[0] + ".jpg"

        if float(lline[1]) < 0.999:
            continue

        if lline[0] in boxmap:
            boxmap[fname].append(data_l)
        else:
            boxmap[fname] = [data_l]
    
    out_jsonfp = open(out_json,"w")
    json.dump(boxmap,out_jsonfp)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: ./output_car_json.py car.txt out.json"
        sys.exit()
    output_car_json(sys.argv[1],sys.argv[2])