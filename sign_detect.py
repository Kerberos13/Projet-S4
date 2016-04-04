# -*- coding: utf-8 -*-

# The aim of this module is to analyse a spectrogram and split it into several pictures according to the presence or not of a signal.
# All of thoses pictures will be saved in a tmp folder and re-used later to rebuild the original image.

import sys, os, numpy
from PIL import Image
from math import floor
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

    if isinstance(picture, Image.Image) :
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

        alpha = floor(255/(pmax - pmin))
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




# This function uses a lowpass filter to limitate possible noise

def denoise(picture) :

    f = numpy.array([[1, 0, 1],
                     [1, 1, 1],
                     [1, 0, 1]])/7

    if isinstance(picture, numpy.ndarray) :
        pic2 = signal.convolve2d(picture, f, boundary = 'symm', mode = 'same')
        pic2 = numpy.floor(pic2)
        return pic2
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
            grad2.append(abs(floor(tmp/v)))

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

    files = os.listdir("tmp/")
    for f in files :
        os.remove("tmp/"+str(f))


    if isinstance(picture,Image.Image) :
        
        files = list()

        spectrogram = numpy.asarray(picture)

        v,h = spectrogram.shape[0],spectrogram.shape[1]
        tmp = grad[0]-grad[1]
        start = list()
        end = list()
        completed = True

        for i in range(0,len(grad)-1) :
            if (abs(tmp) > 40) :
                if completed :
                    start.append(i)
                    completed = False
                else :
                    end.append(i)
                    completed = True

            tmp = -tmp + grad[i-1] - grad[i+1]



        m = 20 # marge in pixels around a given signal
        a = 0
        b = max(start[0]-m,0)
        if (a == b) :
            signal = True
        else :
            signal = False
        i = 1
        j = 0

        #print(start)
        #print(end)

        for k in range(0,2*len(start)-1) :
            #print(a,b,spectrogram.shape[1])
            pic = spectrogram[0:v-1:1,a:b:1]
            #print(spectrogram.shape)
            #print(pic.shape)
            pic2 = Image.fromarray(pic,'RGB')
            a = max(b-m,0)
            if signal :
                if (j < len(end)) :
                    b = min(end[j]+m,h)
                i = i+1
                name = "tmp/"+str(i+j)+"_signal"
            else :
                if (i < len(start)) :
                    b = max(start[i]+m,0)
                j = j+1
                name = "tmp/"+str(i+j)+"_silence"

            signal = not signal
            name = name+".jpg"
            pic2.save(name)
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
                b = floor(a/2)
                a = a - b

                row = numpy.floor(numpy.zeros((1,v,3)))

                for i in range(0,a - 1) :
                   pic2 = vstack(row,pic2)

                for i in range(0,b-1) :
                    pic2 = vstack(pic2,row)

            if (v < dimv) :
                a = dimv - v
                b = floor(a/2)
                a = a - b

                col = numpy.floor(numpy.zeros((h,1,3)))

                for i in range(0,a-1) :
                    pic2 = hstack(col,pic2)

                for i in range(0,b-1) :
                    pic2 = hstack(pic2,col)


            pic = Image.fromarray(pic2,'RGB')
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
    spectrogram2 = denoise(spectrogram2)

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


