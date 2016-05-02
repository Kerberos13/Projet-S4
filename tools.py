# -*- coding: utf-8 -*-

# The aim of this module is to provide generic tools for different modules

import sys, os, numpy
from PIL import Image
from math import floor




# This function displays text on a console like interface if the GUI is started

def printC(text,gui) :
    if gui :
        from gui import printOnConsole
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


