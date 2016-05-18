# -*- coding: utf-8 -*-

# This module should be launched either by the following command "python main.py <filepath>" or by calling its main function in another module as follow "main.main(<filepath>)" where <filepath> is the relative path of a spectrogram

import sys,os,numpy
sys.path.insert(0,'scripts/')

import sign_detect2,reass,resize
import use_CNN_compatible as use_CNN
from tools import *
try :
    import PIL,numpy,scipy,theano
except ImportError :
    print("Pillow, Numpy, Scipy and Theano dependancies must be installed. Try running the setup.py script - Fatal Error.\n")
    sys.exit()



# This is the main function of the whole project and brings it all together

def main(filepath, threshold, margin, boxSize, color) :


    files = sign_detect2.main(os.path.abspath(filepath),margin,threshold,False) # Detection of signals on the spectrogram
    #print(files)

    signals = list()
    for elt in files :
        if (elt[len(elt)-10:] == "signal.bmp" and os.path.exists(elt)) :
            signals.append(elt)
    if len(signals) == 0 :
        print("No signal detected - Error.")
        sys.exit()


    W = 50 # Dimension of the ANN along the horizontal axis (wide)
    H = 37 # Dimension of the ANN along the vertical axis (height)
    
    #CNN_input = numpy.ndarray()
   
    nb = 0
    for elt in signals :

        windows = resize.main(elt,W,H) # Resizing of detected signals

        # CNN_input is a numpy.ndarray object caonting float32 dtype numbers.
        # Each row corresponds to an image of which rows have been concatenated in order to form one long vector - in this case of 50x37 columns
        
        v,h = windows.shape[0],windows.shape[1]
        tmp = numpy.ndarray((1,h),dtype="float32")
        tmp[0,0:h] = windows[0,0:h]
        for i in range(1,v) :
            #print(tmp.shape,windows[i,0:h].shape)
            tmp = numpy.hstack((tmp,windows[i:i+1,0:h]))
          
        if nb == 0 :
            CNN_input = tmp
        else :
            CNN_input = numpy.vstack((CNN_input,tmp))
        nb+=1

        #print(CNN_input.shape)
        

    print("Analysing signals...")

    labels = use_CNN.use_CNN(CNN_input) # Classification of detected signals

    labels2 = list()
    for elt in labels :
        if int(elt) == 0 :
            tmp = "AM"
        if int(elt) == 1 :
            tmp = "FM"
        if int(elt) == 2 :
            tmp = "FSK"
        if int(elt) == 3 :
            tmp = "ASK"
        if int(elt) == 4 :
            tmp = "BLU"
        labels2.append(tmp)

    print("Done.")
    #print(labels2)

    reass.main(labels2,margin,boxSize,color,False) # Reassembly of the different parts for a labeled spectrogram
    
    sys.exit()

    return



# This redirects to the main function

if __name__ == "__main__" :

    N = len(sys.argv)
    
    if N > 1 :
        path = str(sys.argv[1])
        threshold = 2
        margin = 10
        box_width = 4
        color = [250,250,250]
    
        if N >= 3 :
            threshold = int(sys.argv[2])
        if N >= 4 :
            margin = int(sys.argv[3])
        if N >= 5 :
            box_width = int(sys.argv[4])
        if N >= 6 :
            color = int(sys.argv[5])

        main(path,threshold,margin,box_width,color)
        
        if N < 6 :
            print("\nInput arguments missing - Using default values.\n")
    
    else :
        print("\nInput argument missing - Fatal Error.\n")
        sys.exit()



