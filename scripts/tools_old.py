# -*- coding: utf-8 -*-

# The aim of this module is to provide generic tools for different modules

import sys, os, numpy
from PIL import Image
from math import floor




# This function displays text on a console like interface if the GUI is started

def printC(text,gui) :
    if gui :
        if int(sys.version[0]) == 2 :
            from scripts.gui2 import printOnConsole
        elif int(sys.version[0]) == 3 :
            from scripts.gui3 import printOnConsole

        #from gui import printOnConsole
        printOnConsole(text)
        return
    else :
        return


# This function opens an existing spectrogram

def openf(fileName) :

    if (os.path.exists(fileName)) : # We verify that the path is correct
        spectrogram = Image.open(fileName)
        return spectrogram

    else :
        print("Incorrect Path - Fatal Error.\n")
        sys.exit()
        return



# This function closes an existing spectrogram

def closef(picture) :

    if isinstance(picture, Image.Image) : # We verify that we effectively are working on an Image object
        picture.close()
    else :
        print("Wrong Type - Fatal Error.\n")
        sys.exit()
    return



# This function makes it Black and White

def BW(picture) :

    if isinstance(picture,Image.Image) : # We verify that we effectively are working on an Image object
        picture = picture.convert('L')
        picture = numpy.asarray(picture)
        h,v = picture.shape[0],picture.shape[1]
        #picture = (picture[0:h,0:v,0]*1+picture[0:h,0:v,1]*1+picture[0:h,0:v,2]*4)/6
        return picture

    else :
        print("Wrong Type - Fatal Error.\n")
        sys.exit()
        return



# This function makes an RGB picture into a Hue Saturation Value Picture

def HSV(picture) :
    
    if isinstance(picture,Image.Image) : 
        picture = picture.convert('HSV')
        picture = numpy.asarray(picture)
        h,v = picture.shape[0],picture.shape[1]
        picture = picture[0:h,0:v,0]

        return picture

    else :
        print("Wrong Type - Fatal Error.\n")
        sys.exit()
        return



# This functions does zero padding to a given picture (NxMx1 matrix)

def padding1(pic,dimh,dimv) :
    
    v,h = pic.shape[0],pic.shape[1]

    if (h < dimh) : # The picture is currently not wide enough
        a = dimh - h
        b = floor(a/2)
        a = a - b

        col = numpy.zeros((v,1,1),dtype=pic.dtype)

        for i in range(0,a) :
            pic = numpy.concatenate((col,pic),axis=1)

        for i in range(0,b) :
            pic = numpy.concatenate((pic,col),axis=1)

    if (v < dimv) : # The picture is currently not long enough
        a = dimv - v
        b = floor(a/2)
        a = a - b

        row = numpy.zeros((1,h,1),dtype=pic.dtype)

        for i in range(0,a) :
            pic = numpy.concatenate((row,pic),axis=0)

        for i in range(0,b) :
            pic = numpy.concatenate((pic,row),axis=0)

    return pic

    # Note: we do not do anything if the picture is too big. The crop will have to be handled by the second module.




# This functions does zero padding to a given picture (RGB or HSVi NxMx3 matrix)

def padding3(pic,dimh,dimv) :
    
    v,h = pic.shape[0],pic.shape[1]

    if (h < dimh) : # The picture is currently not wide enough
        a = dimh - h
        b = int(floor(a/2))
        a = int(a - b)

        col = numpy.zeros((v,1,3),dtype=pic.dtype)

        for i in range(0,a) :
            pic = numpy.concatenate((col,pic),axis=1)

        for i in range(0,b) :
            pic = numpy.concatenate((pic,col),axis=1)

    if (v < dimv) : # The picture is currently not long enough
        a = dimv - v
        b = int(floor(a/2))
        a = int(a - b)

        row = numpy.zeros((1,h,3),dtype=pic.dtype)

        for i in range(0,a) :
            pic = numpy.concatenate((row,pic),axis=0)

        for i in range(0,b) :
            pic = numpy.concatenate((pic,row),axis=0)

    return pic

    # Note: we do not do anything if the picture is too big. The crop will have to be handled by the second module.




# This function eliminates the possible zero-padding for a NxMx3 matrix

def unpad3(picture,margin) :

    # Because we have margins, we are sure that the signal's dimensions are greater than 1*1 pixel, and because the signal is centered when padded, it is sufficient to analyse the middle row and the middle column to unpad.

    v,h = picture.shape[0],picture.shape[1]

    a = floor(v/2)
    b = floor(h/2)

    picture2 = numpy.asarray(picture)

    for i in range(1,h+1) : # We analyse along the horizontal axis
        if numpy.array_equal(picture[a,h-i,:],[0,0,0]) : # Note: for this equality to be verified, we must use lossless compression algorithms such as bmp and not jpg
            picture2 = numpy.delete(picture2,h-i,1) # We delete the column i

    for i in range(1,v+1) : # We analyse along the vertical axis
        if numpy.array_equal(picture[v-i,b,:],[0,0,0]) :
            picture2 = numpy.delete(picture2,-i,0) # We delete the row i

    return picture2




