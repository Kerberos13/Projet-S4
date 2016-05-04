# -*- coding: utf-8 -*-

# This module should be launched either by the following command "python main.py <filepath>" or by calling its main function in another module as follow "main.main(<filepath>)" where <filepath> is the relative path of a spectrogram


import sys,os,time
import sign_detect2,reass,resize
from tools import *


# This is a mutex, a shared resource with mutual exclusion in order to avoid conflict

class mutex() :

    def __init__(self,value) :
        self.toCancel = value
        self.locked = False
        return

    def set(self,value) :
        self.toCancel = value
        return

    def get(self) :
        return self.toCancel

    def lock(self) :
        i = 0
        while (i<10) : # We allow up to 10 tries
            if self.locked : # The lock has already been taken
                i+=1
                time.sleep(.1)
            else : # The lock is free
                self.locked = True
                return True # Locking was a success
        return False # Locking was a failure

    def unlock(self) :
        self.locked = False
        return
        
global toCancel
toCancel = mutex(False)



# This is the main function of the whole project and brings it all together

def main(filepath, threshold, margin, boxSize, color, gui) :#, toCancel) :


    """
    margin = 12
    boxSize = 6
    color = [120,120,255]
    threshold = 4
    """

    if toCancel.lock() :
        if not toCancel.get() :
            files = sign_detect2.main(filepath,margin,threshold,gui) # Detection of signals on the spectrogram
        toCancel.unlock()
    else :
        print("Aborting Signal detection - Fatal Error")
        printC("Fatal Error: Aborting Signal detection",gui)
        sys.exit()


    time.sleep(.05) # We wait a little to make sure that toCancel has been updated by the dedicated thread

    signals = list()
    for elt in files :
        if (elt[len(elt)-10:] == "signal.bmp" and os.path.exists(elt)) :
            signals.append(elt)
    if len(signals) == 0 :
        print("No signal detected - Error.")
        printC("Error: No signal detected",gui)
        sys.exit()


    W = 50 # Dimension of the ANN along the horizontal axis (wide)
    H = 50 # Dimension of the ANN along the vertical axis (height)
    for elt in signals :

        if toCancel.lock() :
            if not toCancel.get() :
                windows = resize.main(elt,W,H) # Resizing of detected signals
            toCancel.unlock()
        else :
            print("Aborting Signal optimisation - Fatal Error")
            printC("Fatal Error: Aborting Signal optimisation",gui)
            sys.exit()

        time.sleep(.05) # We wait a little to make sure that toCancel has been updated by the dedicated thread
        
    """

        for el in windows :
            if toCancel.lock() :
                if not toCancel.get() :
                        ann.main(el) # Classification of detected signals
                toCancel.unlock()
            else :
                print("Aborting Signal classification - Fatal Error")
                printC("Fatal Error: Aborting Signal classification",gui)
                sys.exit()

            time.sleep(.05) # We wait a little to make sure that toCancel has been updated by the dedicated thread
    """


    if toCancel.lock() :
        if not toCancel.get() :
            reass.main(list(),margin,boxSize,color,gui) # Reassembly of the different parts for a labeled spectrogram
        toCancel.unlock()
    else :
        print("Aborting Reassembly - Fatal Error")
        printC("Fatal Error: Aborting Reassembly",gui)
        sys.exit()

    sys.exit()

    return



# This redirects to the main function

if __name__ == "__main__" :
    if len(sys.argv) == 7 :
        gui = sys.argv[6]
    else :
        gui = False

    if(len(sys.argv)) > 1 :
        if len(sys.argv) >= 7 :
            main(str(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]),gui)
        else :
            print("\nInput arguments missing - Using default values.\n")
            main(str(sys.argv[1]),4,12,6,[250,250,250],gui)
    else :
        print("\nInput argument missing - Fatal Error.\n")
        sys.exit()



