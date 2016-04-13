# -*- coding: utf-8 -*-

# The aim of this module is to reassemble all the parts of a given spectrogram and identify the detected signals in the tmp folder with their corresponding labels

# This module should be launched either by the following command "python reass.py <labels>" or by calling its main function in another module as follow "reass.main(<labels>)"


from PIL import Image
import numpy, os, sys
from gui import printOnConsole as printC


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


    return picture





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

    return picture





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

def main(labels, margin, size, color) :

    files = os.listdir("tmp/")
    files.sort()
    nbSignals = 0
    for elt in files :
        if (elt[len(elt)-1-9:] == "signal.jpg") :
            nbSignals = nbSignals + 1

    if (len(labels) != nbSignals) :
        print("Wrong number of labels - Reassembling without labels\n")
        labels = str("Unknown,"*nbSignals).split(",")

    print("Merging files...\n")
    printC("Mergine files...\n")

    i = 0
    j = 0
    for elt in files :
        
        i = i+1

        print("Processing part "+str(i)+"/"+str(len(files))+"...")
        printC("Processing part "+str(i)+"/"+str(len(files))+"...")
        picture = openf("tmp/"+str(elt))
        picture2 = numpy.asarray(picture)
        if (elt[len(elt)-1-9:] == "signal.jpg") :
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
    printC("\n Cleaning tmp folder...\n")

    clean(files)

    print("Saving final spectrogram...\n")
    printC("Saving final spectrogram...\n")

    pic = Image.fromarray(pic,'RGB')
    pic.save("tmp/spectrogram.jpg")

    print("Done.\n")
    printC("Done.\n")

    sys.exit()

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
        
    main(labels,margin,size,color)

