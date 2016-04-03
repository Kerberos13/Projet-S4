# -*- coding: utf-8 -*-

# The aim of this module is to analyse a spectrogram and split it into several pictures according to the presence or not of a signal.
# All of thoses pictures will be saved in a tmp folder and re-used later to rebuild the original image.

import sys, os, numpy
from PIL import Image
from math import ceil
from scipy import signal


# This function opens an existing spectrogram

def openf(fileName) :

    if (os.path.exists(fileName)) : 
        spectrogram = Image.open(fileName)
        #print(isinstance(spectrogram,Image.Image))
        return spectrogram

    else :
        print("Incorrect Path - Fatal Error.\n")
        sys.exit()
        return




# This function closes an existing spectrogram

def closef(picture) :

    if (type(picture) == Image) :
        picture.close()
    else :
        print("Wrong Type - Fatal Error.\n")
        sys.exit()
    return





# This function makes it Black and White

def BW(picture) :

    if isinstance(picture,Image.Image) :
        picture = picture.convert('L')
        return picture

    else :
        print("Wrong Type - Fatal Error.\n")
        sys.exit()
        return



# This function normalises the pixels' value from 1 to 255 (we want the 0 value to be special)

def norm(picture) :

    if isinstance(picture,Image.Image) :

        picture = numpy.asarray(picture)
        picture.flags.writeable = True
        h,v = picture.shape[0],picture.shape[1]

        pmin = 255
        pmax = 0

        for i in range(0,h-1) :
            for j in range(0,v-1) :
                if (picture[i,j] <= pmin) :
                    pmin = picture[i,j]
                if (picture[i,j] >= pmax) :
                    pmax = picture[i,j]

        alpha = ceil(255/(pmax - pmin))
        beta = pmin - 1

        for i in range(0,h-1) :
            for j in range(0,v-1) :
                picture[i,j] = picture[i,j]*alpha + beta 

        #picture = Image.fromarray(picture,'L')
        
        return picture

    else :
        print("Wrong Type - Fatal Error.\n")
        sys.exit()
        return





# This function calculates the horizontal gradient of the picture

def hgrad(picture) :

    f = numpy.array([[-1, 0, +1],
                     [-1, 0, +1],
                     [-1, 0, +1]])

    if isinstance(picture, numpy.ndarray) :

        grad = signal.convolve2d(picture, f, boundary = 'symm', mode = 'same')
        #print(picture.shape)

        v,h = grad.shape[0],grad.shape[1]
        grad2 =list() 

        for i in range(0,h-1) :
            tmp = 0
            for j in range(0,v-1) :
                tmp = tmp + grad[j,i]
            grad2.append(abs(ceil(tmp/v)))

        #grad2.append(0)
        #print(grad2)

        return grad2

    else :
        print("Wrong Type - Fatal Error.\n")
        sys.exit()
        return





# This function splits the spectrogram into different pictures and save them in a tmp folder

def split(picture, grad) :

    if (os.path.exists("tmp/") == False) :
        os.mkdir('tmp')

    if isinstance(picture,Image.Image) :
        
        files = list()

        spectrogram = numpy.asarray(picture)

        v = spectrogram.shape[0]

        tmp = grad[0]-grad[1]
        start = list()
        end = list()
        completed = False

        for i in range(0,len(grad)-1) :
            if (abs(tmp) > 40) :
                if completed :
                    start.append(i)
                    completed = False
                else :
                    end.append(i)
                    completed = True

            tmp = -tmp + grad[i-1] - grad[i+1]

        a = 0
        b = start[0]
        if (a == b) :
            signal = True
        else :
            signal = False
        i = 0
        j = 0

        print(start)
        print(end)

        for k in range(0,2*len(start)-1) :
            print(a,b,spectrogram.shape[1])
            pic = spectrogram[0:v-1:1,a:b:1]
            #print(spectrogram.shape)
            #print(pic.shape)
            pic2 = Image.fromarray(pic,'RGB')
            a = b
            if signal :
                b = end[j]
                i = i+1
                name = "tmp/signal"+str(j)
            else :
                b = start[i]
                j = j+1
                name = "tmp/silence"+str(i)

            signal = not signal
            pic2.save(name+'.jpg')
            files.append(name)

        return files

    else :
        print("Wrong Type - Fatal Error.\n")
        sys.exit()
        return




# This functions does zero padding to a given picture

def padding(files,dimh,dimv) :

    
    for elt in range(0,len(files)-1) :
        if (os.path.exists(files[elt])) :
            pic = openf(files[elt])

            pic2 = numpy.asarray(pic)
            closef(pic)
            h,v = pic2.shape[0],pic2.shape[1]

            if (h < dimh) :
                a = dimh - h
                b = ceil(a/2)
                a = a - b

                row = ceil(numpy.zeros((1,v)))

                for i in range(0,a - 1) :
                   pic2 = vstack(row,pic2)

                for i in range(0,b-1) :
                    pic2 = vstack(pic2,row)

            if (v < dimv) :
                a = dimv - v
                b = ceil(a/2)
                a = a - b

                col = ceil(numpy.zeros((h,1)))

                for i in range(0,a-1) :
                    pic2 = hstack(col,pic2)

                for i in range(0,b-1) :
                    pic2 = hstack(pic2,col)


            pic = Image.fromarray(pic2,'L')
            pic.save(files[elt])


        else :
            print("Wrong Path - Fatal Error.\n")
            sys.exit()
            return





# This is the main function that brings it all together

def main(filename) :

    dimh = 0;
    dimv = 0;

    print("\nOpening "+str(filename)+"...\n")

    spectrogram = openf(filename)

    print("Optimizing the spectrogram...\n")
    
    spectrogram2 = BW(spectrogram)
    spectrogram2 = norm(spectrogram2)

    print("Detecting signals...\n")
    
    grad = hgrad(spectrogram2)
    files = split(spectrogram, grad)

    print("Optimizing signals...\n")

    padding(files,dimh,dimv)

    print("Closing "+str(filename)+"...\n")

    closef(spectrogram)

    print("Done.\n")

    return



# This redirects to the main function

if __name__ == "__main__" :
    if(len(sys.argv)) > 1 :
        main(str(sys.argv[1]))
    else :
        print("\nMissing arguments - Fatal Error.\n")


