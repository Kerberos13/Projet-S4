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


