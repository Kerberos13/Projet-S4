# -*- coding: utf-8 -*-

# The aim of this module is to generate several versions of a given image with different SNR values
# This module should be launched as follows: python SNR.py <filepath> <SNR_min(dB)> <SNR_max(dB)> <step_value(dB)>


import sys,os,numpy
from math import sqrt,ceil,log
import PIL

sys.path.insert(0,'scripts/')

from tools import *



def main(filepath,SNR_min,SNR_max,SNR_step) :

    pic = openf(filepath)

    if SNR_min > SNR_max or SNR_step < 0 :
        print("Wrong arguments value - Fatal Error.\n")
        return sys.extit()
   

    picture0 = pic.convert('HSV')
 
    picture0 = numpy.asarray(picture0)
    a,b=picture0.shape[0],picture0.shape[1]
    picture = picture0[0:a,0:b,0]

    M = picture.shape[0]*picture.shape[1]
    
    E = numpy.sum(numpy.power(picture,2))/M
 
    N = int(ceil((SNR_max-SNR_min)/SNR_step))+1

    for i in range(0,N) :
       
        print("    Processing image "+str(i)+"/"+str(N)+"...\n")

        SNR = SNR_min+i*SNR_step

        SNR_lin = 10**(float(SNR)/float(10))
        sigma = sqrt(170)*sqrt(E/SNR_lin)

        #print(E,SNR_lin,sigma)
 
        noise = sigma*numpy.random.randn(a,b)
       
        #print(noise,numpy.amin(noise),numpy.amax(noise))

        picture2 = numpy.asarray(picture+(0-numpy.abs(noise)))
        #print(picture2,numpy.amin(picture2),numpy.amax(picture2))

        picture2 = numpy.minimum(numpy.maximum(picture2,0),170)
        picture2 = numpy.asarray(picture2,dtype=numpy.uint8)

        #error = numpy.sum(numpy.power(picture2-picture,2))/M
        #print(sigma,error)

        picture2 = numpy.dstack((picture2,picture0[0:a,0:b,1],picture0[0:a,0:b,2]))
    
        filepath2 = filepath.split(".")
        filepath2[len(filepath2)-2]+="_"+str(SNR)+"dB"
        filepath2 = ".".join(filepath2)

        picture2 = PIL.Image.fromarray(picture2,'HSV')
        picture2 = picture2.convert('RGB')
        picture2.save(filepath2)
 
        #F = numpy.sum(numpy.power(picture,2))/M
        #SNR2 = 10*log(F/error)/log(10)
        #print("SNR",SNR2)


    closef(pic)

    print("    Done.\n")

    return




def analyseWholeFolder(folderpath,SNR_min,SNR_max,SNR_step) :

    if os.path.exists(folderpath) :

        files=os.listdir(folderpath)

        N = len(files)
        i = 1
        for elt in files :
            print("Processing file "+str(i)+"/"+str(N)+"...\n")
            filepath = str(folderpath)+"/"+str(elt)
            if os.path.exists(filepath) :
                main(filepath,SNR_min,SNR_max,SNR_step)
           
            i+=1

    return



if __name__ == "__main__" :
    if len(sys.argv) != 5 :
        print("Wrong number of input arguments - Fatal Error.\n")
        sys.exit()
    else :
        if os.path.isfile(str(sys.argv[1])) :
            main(str(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]))
        elif os.path.isdir(str(sys.argv[1])) :
            analyseWholeFolder(str(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]))
        else :
            print("Wrong path - Fatal Error.\n")


