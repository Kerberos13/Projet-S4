# -*- coding: utf-8 -*-

# The aim of this module is to analyse a spectrogram and split it into several pictures according to the presence or not of a signal.
# All of thoses pictures will be saved in a tmp folder and re-used later to rebuild the original image.

# This module should be launched either by the following command "python sign_detect.py <filePath>" or by calling its main function in another module as follow "sign_detect.main(<filePath>)"

import sys, os, numpy
from PIL import Image
from math import floor
#os.path.insert(0,'scripts/')
from tools import *




# This function returns the temporal mean of the picture as a vector

def vec(picture) :

    if(isinstance(picture,numpy.ndarray)) :
        v,h = picture.shape[0],picture.shape[1]
        vec = list()
        for j in range(0,h) :
            tmp = 0
            for i in range(0,v) :
                tmp = tmp + picture[i,j]
            vec.append(floor(tmp/h))

        return vec

    else :
        print("Wrong type - Fatal Error.\n")
        sys.exit()
        return






# Returns the vector convolution of vec*f

def conv1(vec,f) :

    l = int(floor((len(f)-1)/2))
    m = len(vec)

    vec2 = list()

    for i in range(0,l) :
        vec2.append(vec[i])

    for j in range(l,m-l) :
        tmp = 0
        for i in range(-l,l+1) :
            tmp = tmp + f[l-i]*vec[j+i]
        vec2.append(floor(tmp))
    
    for i in range(m-l,m) :
        vec2.append(vec[i])
   
    return vec2





# This function uses a lowpass filter to limitate possible noise on a vector

def denoise1(vec) :
    
    f = [1./3.,1./3.,1./3.]

    vec2 = conv1(vec,f)

    return vec2



def denoise11(vec) :

    f = [1./9., 1./9., 1./9., 1./9., 1./9., 1./9., 1./9., 1./9., 1./9.]

    vec2 = conv1(vec,f)

    return vec2




# This function calculates the horizontal gradient of the picture

def hgrad1(vec) :

    f = [-1., 0., 1.]

    vec2 = conv1(vec,f)

    return vec2







# This function splits the spectrogram into different parts

def split1(filename,picture,mean,margin,threshold,representation) : # picture must be an Image object, mean must be a list, margin an integer and threshold a float (or an integer)

    
    filename = filename.split(".")
    filename = ".".join(filename[:len(filename)-1])+"_"
    #print("FILENAME",filename)
    filepath2= filename.split("/")
    filepath = list()
    for elt in filepath2 :
        if len(elt) != 0 :
            filepath.append(elt)
    """ 
    TMP = "/"+"/".join(filepath[:len(filepath)-1])+"/tmp/"

    #print("TMP",TMP)

    """
    TMP = "tmp/"


    if (os.path.exists(TMP) == False) : # We create the folder if it does not exist yet
        os.mkdir(TMP)

    files = os.listdir(TMP) # We erase any existing file in the "tmp/" folder as they are supposed to be temporary
    for f in files :
        os.remove(TMP+str(f))


    
    files = list()

    spectrogram = numpy.asarray(picture)

    #print(spectrogram)
    #print(spectrogram.shape)

    v,h = spectrogram.shape[0],spectrogram.shape[1]


    if representation == "BW" : # Case of a BW picture
         
        m = 0
        for elt in mean :
            m = m + elt
        m = m/len(mean)
       
        #print(mean)
        #print(min(mean),m)

        #m = min(mean)

        analyse = list()
        analyse2 = list()
        for k in range(0,h) :
            if (mean[k] > threshold*m) : # Signal detection
                analyse.append(1)
            else :
                analyse.append(0)

            analyse2.append(0)

    elif representation == "HSV" : # Case of the Hue component of an HSV picture

        analyse = list()
        analyse2 = list()
        for k in range(0,h) :
            if ((255-mean[k] < 20*(7-threshold))): # or mean[k] < 5*(7-threshold)) : # The hue is close to pure red
                analyse.append(1)
            else :
                analyse.append(0)

            analyse2.append(0)

    else : # Unknown representation
        print("Unknown Representation - Fatal Error.\n")
        sys.exit()


    #print("ANALYSE",analyse)

    margin = int(floor(margin*len(analyse)/100)+1)


    for i in range(0,margin) :
        if (analyse[i] == 1) :
            for k in range(0,i+margin+1) :
                analyse2[k] = 1

    #print("ANALYSE",analyse)

    for i in range(margin,h-margin) :
        if (analyse[i] == 1) :
            for k in range(i-margin,i+margin+1) :
                analyse2[k] = 1

    #print("ANALYSE",analyse2)

    for i in range(h-margin, h) :
        if (analyse[i] == 1) :
            for k in range(i-margin-1,h) :
                #print(k,h)
                #print("ANALYSE",analyse2)
                analyse2[k] = 1

    #print("ANALYSE",analyse2)

    analyse = analyse2

    tmp = analyse[0]
    a = 0
    b = 0
    nb = 0

    for i in range(0,h): # We actually split the images
        if(analyse[i] == tmp and i < h-1) : # The image continues
            b+=1
        else : # The image changes or ends
            b+=1
            pic = spectrogram[0:v:1,a:b:1,0:3:1]
            name = TMP+filepath[len(filepath)-1]+"0"*(3-len(str(nb)))+str(nb)
            if(analyse[i-1] == 0):# or i == h-1) :
                name += "_silence.bmp"
            else :
                name += "_signal.bmp"
            nb+=1
            tmp = analyse[i]
            a = b
            pic = Image.fromarray(pic,'RGB')
            pic.save(name)
            files.append(name)

    return files





# This is the main function that brings it all together

def main(filename,margin,threshold,gui) :

    #dimh = 50; # Minimum horizontal dimension for zero-padding
    #dimv = 37; # Minimum vertical dimension for zero-padding

    print("\nOpening "+str(filename)+"...\n")

    spectrogram = openf(filename)

    print("Optimizing the spectrogram...\n")
    
    #spectrogram2,representation = BW(spectrogram),"BW"
    #spectrogram2 = numpy.asarray(spectrogram2)

    #spectrogram2 = BW(spectrogram)
    spectrogram2,representation = HSV(spectrogram),"HSV"
    spec = vec(spectrogram2)
    spec = norm1(spec,"inv")
    spec = denoise1(spec)
    #print(spec)

    print("Detecting signals...\n")
    
    files = split1(filename,spectrogram, spec, margin, threshold, representation)

    """
    print("Optimizing signals...\n")
    printC("Optimizing signals...\n",gui)

    padding(files,dimh,dimv)
    """

    print("Closing "+str(filename)+"...\n")

    closef(spectrogram)

    print("Done.\n")

    return files



# This redirects to the main function

if __name__ == "__main__" :

    if len(sys.argv) == 4 :
        gui = sys.argv[3]
    else :
        gui = False

    if (len(sys.argv)) > 1 :
        if (len(sys.arg)) == 3 :
            print("Threshold value missing - Using default value.\n")
            main(str(sys.argv[1]),int(argv[2]),4,gui)
        if (len(sys.arg)) == 4 :
            main(str(sys.argv[1],int(argv[2]),int(argv[3])),gui)
        else :
            print("\nMargin and threshold value missing - Using default values.\n")
            main(str(sys.argv[1]),10,4,gui)
    else :
        print("\nInput argument missing - Fatal Error.\n")


