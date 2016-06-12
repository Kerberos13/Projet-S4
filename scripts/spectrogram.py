# -*- coding: utf-8 -*-

# The aim of this module is to generate a spectrogram from a binary data file

import sys,os
import struct
sys.path.insert(0,'scripts/')

import scipy,PIL,numpy
from math import floor
from tools import *

import wave
from math import *

# This reads a given file

def read(filePath) :
    
    if os.path.exists(filePath) :
        
        f = wave.open(filePath,'rb')
        nbChannels = f.getnchannels()
        nbFrames = f.getnframes()
        a = f.readframes(nbFrames)
        f.close()

        a = numpy.fromstring(a,dtype=numpy.int16)

        #print("NbChannels", nbChannels)
        #print("NbFrames",nbFrames)
        #print("SHAPE",a.shape,nbFrames*nbChannels)
        #print("RAW_DATA",a)

        l = int(a.shape[0])
        if nbChannels == 2 :
            if l%2 == 0 :
                data = a[0:l:2]+1j*a[1:l:2]
            else :
                print("Wrong number of data - Error.\n")
                data = a[0:l-1:2]+1j*a[1:l:2]
        elif nbChannels == 1 :
            data = a
        else :
            print("Unsupported number of channels - Fatal Error.\n")
            sys.exit()

        print("DATA",data)
        print("LENGTH",data.shape)

       
        return data
    
    else :
        print("Wrong Path - Fatal Error.\n")
        sys.exit()
        return



# This generates a signal

def generateSignal() :

    signalI = list()
    signalQ = list()
    N = 2048
    E = 12.

    for i in range(0,N*16) :
        A = E*cos(2*pi*30*i/N)
        B = E*cos(2*pi*300*i/N)
        C = E*sin(2*pi*300*i/N)
        signalI.append(A*B)
        signalQ.append(A*C)
        #print(i,A,B,A*B,cos(pi*i/6))
        
    signalI = numpy.asarray(signalI, dtype=numpy.int16)
    signalQ = numpy.asarray(signalQ, dtype=numpy.int16)

    signal = signalI+1j*signalQ

    #print(signal)

    return signal





# This brings it all together and generates a spectrogram

def main(filePath) :

    print("Reading file...")

    #data = read(filePath)
    data = generateSignal()

    print("Generating spectrogram...")
    
    f,t,spectrogram = scipy.signal.spectrogram(data, nperseg=256, noverlap = 128, scaling = 'density')#, mode = 'magnitude')

    #print("Spectrogram",spectrogram)
 
    spectrogram = 255*(numpy.arctan(0.9*(spectrogram-128)/256)+pi/2)/pi # This transfrom should help detection


    #print("MIN",numpy.amin(spectrogram),"MAX",numpy.amax(spectrogram))
    spectrogram = norm2HSV(spectrogram) # We convert the spectrogram into a Hue matrix
    print("MIN",numpy.amin(spectrogram),"MAX",numpy.amax(spectrogram))


    spectrogram = numpy.asarray(spectrogram,dtype=numpy.uint8)
    spectrogram = spectrogram.transpose()

    #print("Spectrogram",spectrogram)
    #print("SHAPE",spectrogram.shape)
    
    lum = numpy.ones([spectrogram.shape[0],spectrogram.shape[1]],dtype=numpy.uint8)
    #spectrogram = 250*lum
    sat = 255*lum
    lum = 200*lum

    spectrogram = numpy.dstack([spectrogram,sat,lum])
    #spectrogram = numpy.dstack(spectrogram,lum)

    spectrogram = PIL.Image.fromarray(spectrogram,'HSV')
    spectrogram = spectrogram.convert('RGB') 

    filePath2 = filePath.split(".")
    filePath2[len(filePath2)-1] = "jpg"
    filePath2 = ".".join(filePath2)

    spectrogram.save(filePath2)    

    print("Done.")

    return filePath2




if __name__ == "__main__" :
    if len(sys.argv) == 2 :
        main(sys.argv[1])
    else :
        print("Wrong number of input data - Fatal Error.\n")
        sys.exit()



