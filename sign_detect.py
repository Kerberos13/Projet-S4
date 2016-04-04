# -*- coding: utf-8 -*-

# The aim of this module is to analyse a spectrogram and split it into several pictures according to the presence or not of a signal.
# All of thoses pictures will be saved in a tmp folder and re-used later to rebuild the original image.

# This module should be launched either by the following command "python sign_detect.py <filePath>" or by calling its main function in another module as follow "sign_detect.main(<filePath>)"

import sys, os, numpy
from PIL import Image
from math import floor
from scipy import signal


# This function opens an existing spectrogram

def openf(fileName) :

    if (os.path.exists(fileName)) : # We verify that the path is correct
        spectrogram = Image.open(fileName)
        return spectrogram

    else :
        print("Incorrect Path - Fatal Error.\n")
        sys.exit()
        return




# This function closes an existing spectrogram

def closef(picture) :

    if isinstance(picture, Image.Image) : # We verify that we effectively are working on an Image object
        picture.close()
    else :
        print("Wrong Type - Fatal Error.\n")
        sys.exit()
    return





# This function makes it Black and White

def BW(picture) :

    if isinstance(picture,Image.Image) : # We verify that we effectively are working on an Image object
        picture = picture.convert('L')
        return picture

    else :
        print("Wrong Type - Fatal Error.\n")
        sys.exit()
        return



# This function normalises the pixels' value from 1 to 255 (we want the 0 value to be special)

def norm(picture) :

    if isinstance(picture,Image.Image) : # We verify that we effectively are working on an Image object

        picture = numpy.asarray(picture)
        picture.flags.writeable = True # This makes the picture writeable and not read-only
        h,v = picture.shape[0],picture.shape[1] # We get the dimensions of the picture: horizontaly and verticaly

        pmin = 255
        pmax = 0

        for i in range(0,h-1) : # We look for the minimum and maximum pixel value
            for j in range(0,v-1) :
                if (picture[i,j] <= pmin) :
                    pmin = picture[i,j]
                if (picture[i,j] >= pmax) :
                    pmax = picture[i,j]

        alpha = floor(255/(pmax - pmin))
        beta = pmin - 1

        for i in range(0,h-1) : # And we adjust them to improve overall contrast for edge detection
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

    f = numpy.array([[1, 2, 0, 2, 1],
                     [1, 2, 2, 2, 1],
                     [1, 2, 0, 2, 1]])/20 # We use a classical lowpass filter along the horizontal axis

    if isinstance(picture, numpy.ndarray) : # We verify that we effectively are working on a numpy.ndarray object
        pic2 = signal.convolve2d(picture, f, boundary = 'symm', mode = 'same') # We compute the matrix convolution
        pic2 = numpy.floor(pic2) # We make sure that we end up with natural integers
        return pic2
    else :
        print("Wrong Type - Fatal Error.\n")
        sys.exit()
        return




# This function calculates the horizontal gradient of the picture

def hgrad(picture) :

    f = numpy.array([[-1, 0, +1],
                     [-1, 0, +1],
                     [-1, 0, +1]]) # We use a classical gradient filter along the horizontal axis

    if isinstance(picture, numpy.ndarray) : # We verify that we effectively are working on a numpy.ndarray object

        grad = signal.convolve2d(picture, f, boundary = 'symm', mode = 'same') # We compute the matrix convolution
        #print(picture.shape)

        v,h = grad.shape[0],grad.shape[1]
        grad2 =list() 

        for i in range(0,h-1) :
            tmp = 0
            for j in range(0,v-1) :
                tmp = tmp + grad[j,i]
            grad2.append(abs(floor(tmp/v))) # We compute the mean of the gradient along the vertical axis and make sure that we end up with natural integers

        #grad2.append(0)
        #print(grad2)

        return grad2

    else :
        print("Wrong Type - Fatal Error.\n")
        sys.exit()
        return





# This function splits the spectrogram into different pictures and save them in a tmp folder

def split(picture, grad) :

    if (os.path.exists("tmp/") == False) : # We create the folder if it does not exist yet
        os.mkdir('tmp')

    files = os.listdir("tmp/") # We eras any existing file in the "tmp/" folder as they are supposed to be temporary
    for f in files :
        os.remove("tmp/"+str(f))


    if isinstance(picture,Image.Image) : # We verify that we effectively are working on an Image object
        
        files = list()

        spectrogram = numpy.asarray(picture)

        v,h = spectrogram.shape[0],spectrogram.shape[1]
        tmp = grad[0]-grad[1]
        start = list()
        end = list()

        for i in range(0,len(grad)-1) :
            if abs(tmp) > 40 :
                if (len(start) != len(end)) : # End
                    end.append(i)
                else : # Start
                    if (len(end) != 0 and i - end[len(end)-1] < 5) :
                        end.pop()
                    else :
                        start.append(i)

            tmp = -tmp + grad[i-1] - grad[i+1]
        

        """
        v,h = spectrogram.shape[0],spectrogram.shape[1]
        tmp = grad[0]-grad[1]
        start = list()
        end = list()
        completed = True
        keepOn = False

        
        for i in range(0,len(grad)-1) : # We decide when a signal starts and ends
            if (abs(tmp) > 40) :
                print(i,completed,keepOn)
                if completed :
                    if (len(end) != 0 and end[len(end)-1] - i < 10) : # If the start is less than 10 pixels away from the last end, we decide it is in fact part of the same signal and we keep on
                        keepOn = True
                    else :
                        keepOn = False
                        start.append(i) # It is really two distinct signals
                    completed = False
                else :
                    if keepOn :
                        end[max(0,len(end)-1)] = i # We update the end of the signal
                    else :
                        end.append(i) # We store the end of this new signal
                    completed = True

            tmp = -tmp + grad[i-1] - grad[i+1]
        """


        m = 10 # marge in pixels around a given signal
        a = 0
        b = max(start[0]-m,0)
        if (a == b) :
            signal = True
        else :
            signal = False
        i = 1
        j = 0


        for k in range(0,2*len(start)) : # We actually split the original image according to the horizontal gradient calculated on the Black&White copy
            pic = spectrogram[0:v-1:1,a:b:1]
            pic2 = Image.fromarray(pic,'RGB')
            a = max(b-m,0)
            if signal :
                if (j < len(end)) :
                    b = min(end[j]+m,h)
                i = i+1
                tau = str(i+j-2)
                name = "tmp/"+"0"*(3-len(tau))+tau+"_signal"
            else :
                if (i < len(start)) :
                    b = max(start[i]+m,0)
                j = j+1
                tau = str(i+j-2)
                name = "tmp/"+"0"*(3-len(tau))+tau+"_silence"

            signal = not signal
            name = name+".jpg"
            pic2.save(name)
            files.append(name) # We save those images in the "tmp/" folder


        pic2 = Image.fromarray(spectrogram[0:v-1:1,a:h-1:1],'RGB')
        tau = str(i+j-1)
        name = "tmp/"+"0"*(3-len(tau))+tau+"_silence.jpg"
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
        if (os.path.exists(files[elt])) : # We verify that the path is correct
            pic = openf(files[elt])

            pic2 = numpy.asarray(pic)
            closef(pic)
            h,v = pic2.shape[0],pic2.shape[1]

            if (h < dimh) : # The picture is currently not wide enough
                a = dimh - h
                b = floor(a/2)
                a = a - b

                row = numpy.floor(numpy.zeros((1,v,3)))

                for i in range(0,a - 1) :
                   pic2 = numpy.vstack(row,pic2)

                for i in range(0,b-1) :
                    pic2 = numpy.vstack(pic2,row)

            if (v < dimv) : # The picture is currently not long enough
                a = dimv - v
                b = floor(a/2)
                a = a - b

                col = numpy.floor(numpy.zeros((h,1,3)))

                for i in range(0,a-1) :
                    pic2 = hstack(col,pic2)

                for i in range(0,b-1) :
                    pic2 = hstack(pic2,col)


            pic = Image.fromarray(pic2,'RGB')
            pic.save(files[elt]) # We save the resulting files over the originals

            # Note: we do not do anything if the picutre is too big. The crop will have to be handled by the second module.

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

    #spectrogram.show()

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
        print("\nInput argument missing - Fatal Error.\n")


