# -*- coding: utf-8 -*-

# The aim of this module is to reassemble all the parts of a given spectrogram and identify the detected signals in the tmp folder with their corresponding labels

# This module should be launched either by the following command "python reass.py <labels>" or by calling its main function in another module as follow "reass.main(<labels>)"


from PIL import Image, ImageFont, ImageDraw
import numpy, os, sys
#os.path.insert(0,'scripts/')
from math import floor
from tools import *





# This function draw a box of the given color around the signal

def box(picture, color, size) : # Color is a list of the RGB components, size is in pixels

    v,h = picture.shape[0],picture.shape[1]

    picture.flags.writeable = True

    for i in [0,1,2] : # Need to check first two coordinates...
        picture[0:v:1,0:size-1:1,i] = color[i]
        picture[0:v:1,h-size+1:h:1,i] = color[i]
        picture[0:size-1:1,0:h:1,i] = color[i]
        picture[v-size+1:v:1,0:h:1,i] = color[i]
        
    return picture





# This function prints a label near the corresponding signal

def lbl(picture,label,color,size) :

    if isinstance(picture, numpy.ndarray ) :

        picture = Image.fromarray(picture,'RGB')
        draw = ImageDraw.Draw(picture)

        # font = ImageFont.truetype(<font-file>, <font-size>)
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", int(3*size))
        #font = ImageFont.load_default()

        txt = str()
        for elt in label :
            txt += str(elt+"\n")

        # draw.text((x, y),"Sample Text",(r,g,b))
        draw.text((int(2+size), int(2+size)),txt,tuple(color),font=font) # Note: color should be a tuple
        
        picture = numpy.asarray(picture)

        return picture

    else :

        print("Wrong Type - Fatal Error.\n")
        sys.exit()

        return




# This function cleans the tmp folder

def clean(files) :
    
    for elt in files :
        if os.path.exists("tmp/"+str(elt)) :
            os.remove("tmp/"+str(elt))            
    return





# This is the main function that brings it all together

def main(labels, margin, size, color,gui) :

    files = os.listdir("tmp/")
    files.sort()
    nbSignals = 0
    for elt in files :
        if (elt[len(elt)-1-9:] == "signal.bmp") :
            nbSignals = nbSignals + 1

    """
    if not os.path.exists("tmp/lbl.txt") : # We verify that the file exists
        print("Wrong Path - Reassembling without labels")
    else :
        labels = open("tmp/lbl.txt",'r')
        labels = labels.split("\n")
    """

    if (len(labels) != nbSignals) :
        print("Wrong number of labels - Reassembling without labels\n")
        labels = str("Unknown,"*nbSignals).split(",")

    print("Merging files...\n")

    i = 0
    j = 0
    for elt in files :
        
        i = i+1

        print("Processing part "+str(i)+"/"+str(len(files))+"...")
        picture = openf("tmp/"+str(elt))
        picture2 = numpy.asarray(picture)
        if (elt[len(elt)-1-9:] == "signal.bmp") :
            #picture2 = unpad3(picture2,margin)
            picture2 = box(picture2, color, size)
            picture2 = lbl(picture2, labels[j], color, size)
            j = j + 1
        if (i == 1) :
            pic = picture2
        else :
            #print(pic.shape,picture2.shape)
            pic = merge(pic,picture2)
        closef(picture)

    print("\nCleaning tmp folder...\n")

    clean(files)

    print("Saving final spectrogram...\n")

    pic = Image.fromarray(pic,'RGB')
    pic.save("tmp/spectrogram.jpg")

    print("Done.\n")

    return





# This redirects to the main function

if __name__ == "__main__" :

    if(len(sys.argv)) == 1 :
        print("\nInput argument missing - Reassembling without labels\n")
        labels = list()
    else :
        labels = str(sys.argv[1])

    if(len(sys.argv) >= 2) :
        print("\nMargin value missing - Using default value.\n")
        margin = 5
    else :
        margin = int(sys.argv[2])

    if(len(sys.argv) >= 3) :
        print("\nSize value missing - Using default value.\n")
        size = 4
    else :
        size = int(sys.argv[3])

    if(len(sys.argv) >= 4) :
        print("\nColor value missing - Using default value.\n")
        color = [120,120,250]
    else :
        color = int(sys.argv[4])
        
    if len(sys.argv) == 5 :
        gui = sys.argv[4]
    else :
        gui = False

    main(labels,margin,size,color,gui)

