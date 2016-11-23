
import matplotlib  
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'

import numpy as np
import os
os.chdir('..')
caffe_root = './'

import sys
sys.path.insert(0, caffe_root + 'python')
import time

import caffe
from caffe.proto import caffe_pb2

caffe.set_device(0)
caffe.set_mode_gpu()

solver = caffe.SGDSolver(caffe_root + 'models/VGGNet/VOC0712/SSD_300x300/solver.prototxt')
solver.net.copy_from(caffe_root + 'models/VGGNet/VGG_ILSVRC_16_layers_fc_reduced.caffemodel')


transformer = caffe.io.Transformer({'data': solver.net.blobs['data'].data.shape})
transformer.set_transpose('data', (2, 0, 1))
transformer.set_mean('data', np.array([104,117,123])) # mean pixel
transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

net = solver.net

from google.protobuf import text_format
from caffe.proto import caffe_pb2

labelmap_file = 'data/ShenZhou/labelmap_voc.prototxt'
file = open(labelmap_file, 'r')
labelmap = caffe_pb2.LabelMap()
text_format.Merge(str(file.read()), labelmap)

print labelmap

def get_labelname(labelmap, labels):
    print labels
    num_labels = len(labelmap.item)
    labelnames = []
    if type(labels) is not list:
        labels = [labels]
    for label in labels:
        found = False
        for i in xrange(0, num_labels):
            if label == labelmap.item[i].label:
                found = True
                labelnames.append(labelmap.item[i].display_name)
                break
        assert found == True
    return labelnames

solver.step(1)

colors = plt.cm.hsv(np.linspace(0, 1, 21)).tolist()

img_blob = net.blobs['data'].data
#num_imgs = img_blob.shape[0]
num_imgs = 2
img_width = img_blob.shape[2]
img_height = img_blob.shape[3]
label_blob = net.blobs['label'].data[0,0,:,:]
num_labels = label_blob.shape[0]

print label_blob

for i in xrange(num_imgs):
    img = transformer.deprocess('data', img_blob[i])
    plt.subplot(1, num_imgs, i + 1)
    plt.imshow(img)
    currentAxis = plt.gca()
    for j in xrange(num_labels):
        gt_bbox = label_blob[j, :]
        if gt_bbox[0] == i:
            xmin = gt_bbox[3] * img_width
            ymin = gt_bbox[4] * img_height
            xmax = gt_bbox[5] * img_width
            ymax = gt_bbox[6] * img_height
            gt_label = int(gt_bbox[1])
            coords = (xmin, ymin), xmax - xmin + 1, ymax - ymin + 1
            color = colors[gt_label]
            currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=2))
            label = get_labelname(labelmap, gt_label)[0]
            currentAxis.text(xmin, ymin, label, bbox={'facecolor':color, 'alpha':0.5})

plt.savefig("test.png")