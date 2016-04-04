# -*- coding: utf-8 -*-

# This module should be launched either by the following command "python main.py <filepath>" or by calling its main function in another module as follow "main.main(<filepath>)" where <filepath> is the relative path of a spectrogram


import sys

import sign_detect,reass



# This is the main function of the whole project and brings it all together

def main(filepath) :

    sign_detect.main(filepath) # Detection of signals on the spectrogram

    reass.main(list()) # Reassembly of the different parts for a labeled spectrogram

    return



# This redirects to the main function

if __name__ == "__main__" :
    if(len(sys.argv)) > 1 :
        main(str(sys.argv[1]))
    else :
        print("\nInput argument missing - Fatal Error.\n")
        sys.exit()

