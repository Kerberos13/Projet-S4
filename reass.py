# -*- coding: utf-8 -*-

# The aim of this module is to reassemble all the parts of a given spectrogram and identify the detected signals in the tmp folder with their corresponding labels

# This module should be launched either by the following command "python reass.py <labels>" or by calling its main function in another module as follow "reass.main(<labels>)"


from PIL import Image, ImageFont, ImageDraw
import numpy, os, sys
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





# This function eliminates the possible zero-padding

def unpad(picture,margin) :

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

def lbl(picture,label,color) :

    if isinstance(picture, numpy.ndarray ) :

        picture = Image.fromarray(picture,'RGB')
        draw = ImageDraw.Draw(picture)

        # font = ImageFont.truetype(<font-file>, <font-size>)
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 12)

        # draw.text((x, y),"Sample Text",(r,g,b))
        draw.text((3, 2),label,tuple(color),font=font) # Note: color should be a tuple
        
        picture = numpy.asarray(picture)

        return picture

    else :

        print("Wrong Type - Fatal Error.\n")
        sys.exit()

        return





# This function merges the picture ndarray at the right of the pic ndarray

def merge(pic,picture) :
 
    pic = numpy.hstack((pic,picture))

    return pic





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

    if not os.path.exists("tmp/lbl.txt") : # We verify that the file exists
        print("Wrong Path - Reassembling without labels")
        printC("Wrong Path - Reassembling without labels",gui)
    else :
        labels = open("tmp/lbl.txt",'r')
        labels = labels.split("\n")


    if (len(labels) != nbSignals) :
        print("Wrong number of labels - Reassembling without labels\n")
        printC("Wrong number of labels - Reassembling without labels",gui)
        labels = str("Unknown,"*nbSignals).split(",")

    print("Merging files...\n")
    printC("Merging files...\n",gui)

    i = 0
    j = 0
    for elt in files :
        
        i = i+1

        print("Processing part "+str(i)+"/"+str(len(files))+"...")
        printC("Processing part "+str(i)+"/"+str(len(files))+"...",gui)
        picture = openf("tmp/"+str(elt))
        picture2 = numpy.asarray(picture)
        if (elt[len(elt)-1-9:] == "signal.bmp") :
            picture2 = unpad(picture2,margin)
            picture2 = box(picture2, color, size)
            picture2 = lbl(picture2, labels[j], color)
            j = j + 1
        if (i == 1) :
            pic = picture2
        else :
            pic = merge(pic,picture2)
        closef(picture)

    print("\nCleaning tmp folder...\n")
    printC("\n",gui)
    printC("Cleaning tmp folder...\n",gui)

    clean(files)

    print("Saving final spectrogram...\n")
    printC("Saving final spectrogram...\n",gui)

    pic = Image.fromarray(pic,'RGB')
    pic.save("tmp/spectrogram.jpg")

    print("Done.\n")
    printC("Done.\n",gui)

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

