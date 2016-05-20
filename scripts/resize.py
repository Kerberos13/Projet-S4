# -*- coding: utf-8 -*-

# The aim of this module is to split and resize portions of a spectrogram according to usable dimensions by the neuronal network
# All of thoses pictures will be loaded in the RAM as they will only be used by the ANN.

import sys, os, numpy
from PIL import Image
from math import floor
#os.path.insert(0,'scripts/')
from tools import *




# This function resizes the picture if needed (but conserves original ratio)

def resize(picture,W,H) :


    if isinstance(picture, Image.Image) : # We verify that we effectively are working on an Image.Image object
        #h,v = picture.size[0],picture.size[1]
        #W = int(W*floor(h/W))
        #H = int(H*floor(v/H))

        picture = picture.resize((W,H),Image.ANTIALIAS)
        return picture
    else :
        print("Wrong Type - Fatal Error.\n")
        sys.exit()
        return


"""
# This function splits the picture into several parts, directly usable by the ANN

def split(picture,W,H) :

    if isinstance(picture,numpy.ndarray) :

        h,v = picture.shape[0],picture.shape[1]
        windows = list()

        if h > W : # Horizontal axis (Width)
            m = int(floor(h/W))
        else :
            m = 1

        if v > H : # Vertical axis (Height)
            p = int(floor(v/H))
        else :
            p = 1

        for k in range(0,m) :
            for l in range(0,p) :
                windows.append(picture[k*W:(k+1)*W-1,l*H:(l+1)*H-1])

        return windows

    else :
        print("Wrong Type - Fatal Error.\n")
        sys.exit()
        return
"""


# This is the main function that brings it all together

def main(signal,W,H) :

    # First, we open the file

    picture = openf(signal)

    # We do some optionnal zero-padding

    pic = numpy.asarray(picture)
    pic = padding3(pic,W,H)
    pic = Image.fromarray(pic,'RGB')

    # We resize it

    picture = resize(pic,W,H)

    # We convert the RGB picture to a hue matrix

    pic = BW(picture)
    pic = Image.fromarray(pic,'L')
    pic = norm2(pic)
    closef(picture)

    #pic = Image.fromarray(pic,'L')
    #pic.save("test2/test.bmp")

    pic = numpy.asarray(pic)

    # And finally, we split it into 50x50 small pieces that we return as a list of numpy.ndarray
    #windows = split(pic,W,H)

    return pic

