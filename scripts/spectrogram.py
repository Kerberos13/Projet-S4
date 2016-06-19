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
        
        f = wave.open(filePath,'rb') # We use the wave library to read .wav files efficiently
        nbChannels = f.getnchannels()
        nbFrames = f.getnframes()
        a = f.readframes(nbFrames)
        f.close()

        a = numpy.fromstring(a,dtype=numpy.int16) # We convert the byte stream into a numpy array

        l = int(a.shape[0])
        if nbChannels == 2 : # We then convert it to a complex signal according to the number of channels
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
       
        return data
    
    else :
        print("Wrong Path - Fatal Error.\n")
        sys.exit()
        return



# This generates a signal

def generateSignal() :

    signalI = list()
    signalQ = list()
    N = 2**13
    E = 12.

    for i in range(0,N*16) :
        A = E*cos(2*pi*30*i/N)
        B = E*cos(2*pi*300*i/N)
        C = E*sin(2*pi*300*i/N)
        signalI.append(A*B)
        signalQ.append(A*C)
        
    signalI = numpy.asarray(signalI, dtype=numpy.int16)
    signalQ = numpy.asarray(signalQ, dtype=numpy.int16)

    signal = signalI+1j*signalQ

    return signal




# This removes the artefacts

def removeArtefacts(spectrogram, max_size, l) :

    h = list()
    n = 2*l+2*max_size-1
    for i in range(0,n) : # We generate the convolution filter
        if i <= l-1 :
            h.append(exp(-(8*(l/2-i)/l)**2))
        elif i >= n-l :
            h.append(exp(-(8*(l/2-(n-i))/l)**2))
        else :
            h.append(0.)
    
    h = numpy.asarray(h)
    h = numpy.vstack((h,h,h))

    p = numpy.sum(h,(0,1)) # We norm the convolution filter
    h = h/p

    #print(numpy.sum(h,(0,1)))
    #print(h)

    spectrogram = scipy.signal.convolve2d(spectrogram, h, boundary='symm', mode='same')

    spectrogram = numpy.asarray(spectrogram, dtype = numpy.uint8) # We convert the result back to a numpy array, directly usable by the PIL library

    #print(numpy.sum(spectrogram,(0,1)))

    return spectrogram




# This detects artefacts

def detectArtefacts(spectrogram, max_size, threshold) :

    tmp = vec(spectrogram) # We start by computing the mean along the time axis
    tmp = norm1(tmp,"inv")
    tmp = denoise1(tmp)
    h = len(tmp)

    analyse0 = list()
    analyse2 = list()
    signals = list()
    for k in range(0,h) :
        if ((255-tmp[k] < 20*(7-threshold))): # The hue is close to pure red
            analyse0.append(1)
        else :
            analyse0.append(0)
        analyse2.append(0)
        signals.append(0)

    #print(analyse0)

    analyse = list(analyse0)
    for i in range(0,h) :
        if (analyse[i] == 1) :
            for k in range(i,h) :
                if ((analyse0[k] == 0) or (k == h-1)) :
                    if (abs(k-i) <= max_size) : # We only consider small enough signals that can be artefacts
                        for l in range(i,k+1) :
                            analyse[l] = 1
                    else :
                        for l in range(i,k+1) :
                            analyse[l] = 0
                            signals[l] = 1
                    break

    
    l = 9 # 2*3*l is the number of points on which the new hue value will be calculated
    Width = 2*(l+max_size) - 1 + max_size - 1 # This is the width of the extracted matrices
    margin = l+max_size-1

    #print("ANALYSE",analyse)

    for i in range(0,margin) :
        if (analyse[i] == 1) :
            new_signal = False
            for k in range(0,margin) :
                if signals[k] == 1 :
                    new_signal = True
            if not new_signal :
                for k in range(0,i+margin+1) :
                    analyse2[k] = 1


    for i in range(margin,h-margin) :
        if (analyse[i] == 1) :
            new_signal = False
            for k in range(i-margin,i+margin+1) :
                if signals[k] == 1 :
                    new_signal = True

            if not new_signal :
                for k in range(i-margin,i+margin+1) :
                    analyse2[k] = 1


    for i in range(h-margin, h) :
        if (analyse[i] == 1) :
            new_signal = False
            for k in range(i-margin-1,h) :
                if signals[k] == 1 :
                    new_signal = True
            if not new_signal :
                for k in range(i-margin-1,h) :
                    analyse2[k] = 1

    #print("ANALYSE",analyse2)

    analyse = analyse2

    tmp = analyse[0]
    a = 0
    b = 0
    nb = 0
    v = spectrogram.shape[0]
    for i in range(0,h): # We actually split the images
        if(analyse[i] == tmp and i < h-1) : # The image continues
            b+=1
        else : # The image changes or ends
            b+=1
            pic = spectrogram[0:v:1,a:b:1]
            if(analyse[i-1] == 0):# or i == h-1) :
                pass
            else :
                pic = removeArtefacts(pic, max_size, l)
            if nb == 0 :
                spectrogram2 = pic
            else :
                spectrogram2 = merge(spectrogram2,pic)
            tmp = analyse[i]
            a = b
            nb+=1
    

    return spectrogram2





# If a signal is splitted on the edges of the spectrogram, it is then reassembled into one piece

def centering(spectrogram, threshold, margin) :

    mean = vec(spectrogram) # We start by computing the mean along the time axis
    mean = norm1(mean,"inv")
    mean = denoise1(mean)
    h = len(mean)
    v = spectrogram.shape[0]

    analyse = list()
    analyse2 = list()
    for k in range(0,h) :
        if ((255-mean[k] < 20*(7-threshold))): # The hue is close to pure red
            analyse.append(1)
        else :
            analyse.append(0)

        analyse2.append(0)

    margin = int(floor(margin*len(analyse)/100)+1)

    for i in range(0,margin) :
        if (analyse[i] == 1) :
            for k in range(0,i+margin+1) :
                analyse2[k] = 1

    for i in range(margin,h-margin) :
        if (analyse[i] == 1) :
            for k in range(i-margin,i+margin+1) :
                analyse2[k] = 1

    for i in range(h-margin, h) :
        if (analyse[i] == 1) :
            for k in range(i-margin-1,h) :
                analyse2[k] = 1

    analyse = analyse2

    if analyse[0] == 1 or analyse[h] == 1 : # A signal is splitted
        i = 0
        while analyse[i] != 0 and i < margin :
            i+=1
        spectrogram2 = merge(spectrogram[0:v,i:h],spectrogram[0:v,0:i])


    return spectrogram2





# This brings it all together and generates a spectrogram

def main(filePath, threshold, margin) :

    print("Reading file...")

    data = read(filePath)
    #data = generateSignal()

    print("Generating spectrogram...")
    
    f,t,spectrogram = scipy.signal.spectrogram(data, nperseg=512, scaling = 'density')

    spectrogram = norm2log(spectrogram) # We use a log norm to retrieve the signals among the noise
    spectrogram = 255*(numpy.arctan(10*(spectrogram-128)/256)+pi/2)/pi # This transfrom should help detection by maximizing mid-tones details
    spectrogram = norm2HSV(spectrogram) # We convert the spectrogram into a Hue matrix

    spectrogram = numpy.asarray(spectrogram,dtype=numpy.uint8)
    spectrogram = spectrogram.transpose()

    lum = numpy.ones([spectrogram.shape[0],spectrogram.shape[1]],dtype=numpy.uint8) # We now assemble the complete spectrogram picture
    sat = 255*lum
    lum = 200*lum

    spectrogram = numpy.dstack([spectrogram,sat,lum])
    spectrogram = PIL.Image.fromarray(spectrogram,'HSV')
    spectrogram = spectrogram.resize((800,600),PIL.Image.ANTIALIAS) # And we resize it to be able 1) to save it and 2) to reduce the computation time


    print("Removing artefacts...")
 
    spectrogram = numpy.asarray(spectrogram,dtype=numpy.uint8)
    a,b = spectrogram.shape[0],spectrogram.shape[1]
    
    max_size = int(ceil(8.*(800./1200.))) # This is the constated average artefact size, relatively to the spectrogram's size
    #print("MAX_SIZE",max_size)

    spectrogram2 = spectrogram[0:a:1,0:b:1,0]
    spectrogram2 = centering(spectrogram2, threshold, margin) # We make sure that no signal is splitted in our spectrogram
    spectrogram2 = detectArtefacts(spectrogram2, max_size, threshold) # And we detect and remove any possible artefacts
    
    spectrogram = numpy.dstack([spectrogram2,spectrogram[0:a,0:b,1],spectrogram[0:a,0:b,2]])
    spectrogram = PIL.Image.fromarray(spectrogram,'HSV')
    spectrogram = spectrogram.convert('RGB') # Conversion to RGB representation is necessary when saving as jpg with PIL
    

    filePath2 = filePath.split(".")
    filePath2[len(filePath2)-1] = "jpg"
    filePath2 = ".".join(filePath2)

    spectrogram.save(filePath2)    

    print("Done.")

    return filePath2




if __name__ == "__main__" :
    if len(sys.argv) == 3 :
        main(str(sys.argv[1]),int(sys.argv[2]))
    else :
        print("Wrong number of input data - Fatal Error.\n")
        sys.exit()



