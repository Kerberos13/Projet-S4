# -*- coding: utf-8 -*-

# The aim of this module is to convert every bmp file into a jpg file in a given folder

# This module should be launched by the following command "python tojpg.py <folderPath>"

import sys, os
from PIL import Image
from tools import *



def main(folderPath) :

    if not os.path.exists(folderPath) :
        print("Wrong Path - Fatal Error.\n")
        sys.exit()
    else :

        files = os.listdir(folderPath)
        files2 = list()
        for elt in files :
            if len(elt) != 0 and (elt.endswith(".bmp")) :
                files2.append(folderPath+"/"+elt)

        i = 1
        for elt in files2 :
            image = openf(elt)
            name = elt[:len(elt)-4]
            image.save(name+".jpg")
            closef(image)
            print(str(i)+"/"+str(len(files2)))
            i+=1

    return




if __name__ == "__main__" :
    if len(sys.argv) != 2 :
        print("Wrong number of input arguments - Fatal Error.\n")
        sys.exit()
    else :
        main(str(sys.argv[1]))

