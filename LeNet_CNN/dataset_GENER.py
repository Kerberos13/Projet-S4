__author__ = 'yxu01'
import sys
import os
import numpy
from PIL import Image
import cPickle
import gzip

#fuction copyed from sign_detect2, Benoit
def openf(fileName) :
    #thumbnail is a 28*28(changeable) image
    if (os.path.exists(fileName)) : # We verify that the path is correct,
        thumbnail = Image.open(fileName)
        return thumbnail

    else :
        print("Incorrect Path - Fatal Error.\n")
        sys.exit()
        return
def BW(picture) :

    if isinstance(picture,Image.Image) : # We verify that we effectively are working on an Image object
        picture = picture.convert('L')
        return picture

    else :
        print("Wrong Type - Fatal Error.\n")
        sys.exit()
        return

def saveData(image,fileName="./single_image.pkl.gz",batch_size =500):
    bw_image = BW(image)
    bw_image.save('bw.jpg')
    bw_image = numpy.asarray(bw_image,dtype='float32')
    bw_image = bw_image/numpy.max(bw_image)
    bw_image = bw_image.flatten()
    #copy each row to fit the batch_size
    c= numpy.tile(bw_image,(batch_size,1))
    with gzip.open(fileName, 'wb') as f:
        cPickle.dump([c], f)
    return 0


