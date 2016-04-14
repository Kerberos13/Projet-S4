# -*- coding: utf-8 -*-

# This module should be launched either by the following command "python main.py <filepath>" or by calling its main function in another module as follow "main.main(<filepath>)" where <filepath> is the relative path of a spectrogram


import sys,os

import sign_detect2,reass



# This is the main function of the whole project and brings it all together

def main(filepath, threshold, margin, boxSize, color, gui) :

    """
    margin = 12
    boxSize = 6
    color = [120,120,255]
    threshold = 4
    """

    sign_detect2.main(filepath,margin,threshold,gui) # Detection of signals on the spectrogram

    reass.main(list(),margin,boxSize,color,gui) # Reassembly of the different parts for a labeled spectrogram

    """
    if os.path.exists("tmp/spectrogram.jpg") :
        gui.disp_pic("tmp/spectrogram.jpg")
    else :
        print("Fatal Error.\n")
    """

    sys.exit()

    return



# This redirects to the main function

if __name__ == "__main__" :
    if len(sys.argv) == 7 :
        gui = sys.argv[6]
    else :
        gui = False

    if(len(sys.argv)) > 1 :
        if len(sys.argv) >= 6 :
            main(str(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]),gui)
        else :
            print("\nInput arguments missing - Using default values.\n")
            main(str(sys.argv[1]),4,12,6,[120,120,250],gui)
    else :
        print("\nInput argument missing - Fatal Error.\n")
        sys.exit()


