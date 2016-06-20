# -*- coding: utf-8 -*-


# This script aims at simplifying the consruction of the database
# It basically launches the first part of the main function in order to detext signals and resize these windows in order to train the neuronal network

# It should be launched with the following command line: python detect&resize.py <FolderToExplore> <ThresholdValue> <MarginValue> <WidthDimension> <HeightDimension>


import os,sys
#os.path.insert(0,'scripts/')
import sign_detect2,resize
from PIL import Image
from math import ceil


def main(Folder, threshold, margin, Width,Height) :

    gui = False

    if not os.path.exists(Folder) or threshold < 2 or margin < 2 or Width < 10 or Height < 10 :
        print("Wrong Argument - Fatal Error.\n")
        sys.exit()
        return

    files = os.listdir(Folder)
    files2 = list()
    for elt in files :
        if len(elt) != 0 and (elt.endswith(".jpg")) :# or elt.endswith(".bmp")) :
            files2.append(Folder+"/"+elt)

    i = 0
    for filepath in files2 :
        
        print("Progress: "+str(float(ceil(1000*float(i)/float(len(files2)))/10))+"%")

        fils = sign_detect2.main(filepath,margin,threshold,gui) # Detection of signals on the spectrogram


        signals = list()
        for elt in fils :
            if (elt[len(elt)-10:] == "signal.bmp" and os.path.exists(elt)) :
                signals.append(elt)
        if len(signals) == 0 :
            print("No signal detected - Error.")
            next


        for elt in signals :
            window = resize.main(elt,Width,Height) # Resizing of detected signals
            window = Image.fromarray(window,'L')
            name = elt.split("/")
            path = filepath.split("/")
            path = "/".join(path[:len(path)-1])
            name = path+"/resized_"+name[len(name)-1]
            window.save(name)


        for elt in fils :
            os.remove(elt)

        i+=1

    return



if __name__ == "__main__" :
    if len(sys.argv) == 6 :
        main(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]))
    else :
        print("Input argument missing - Fatal Error.\n")
        sys.exit()

