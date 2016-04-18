# -*- coding: utf-8 -*-

# The aim of this module is to analyse a spectrogram and split it into several pictures according to the presence or not of a signal.
# All of thoses pictures will be saved in a tmp folder and re-used later to rebuild the original image.

# This module should be launched either by the following command "python sign_detect.py <filePath>" or by calling its main function in another module as follow "sign_detect.main(<filePath>)"

import sys, os, numpy
from PIL import Image
from math import floor
from scipy import signal
#from gui import printOnConsole



# This function displays text on a console like interface if the GUI is started

def printC(text,gui) :
    if gui :
        from gui import printOnConsole
        printOnConsole(text)
        return
    else :
        return


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





# This functions crops the original picture to get rid of the white frame around the spectrogram in itself
# Note : one possibility would be to save the frame in order to remerge it with the final image later

def crop(picture) :


    return picture





# This function normalises the pixels' value from 1 to 255 from a picture - We want 0 to be reserved for the zero-padding

def norm2(picture) :

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

        if(pmin != 1 and pmax != 255) :
            alpha = floor(255/(pmax - pmin))
            beta = pmin

            for i in range(0,h) : # And we adjust them to improve overall contrast for edge detection
                for j in range(0,v) :
                    picture[i,j] = (picture[i,j] - beta)*alpha

            #picture = Image.fromarray(picture,'L')
    
        return picture

    else :
        print("Wrong Type - Fatal Error.\n")
        sys.exit()
        return





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





# This functions normalizes the pixels' value from 0 to 255 from a list

def norm1(vec,s) :

    pmin = min(vec)
    pmax = max(vec)
    alpha = floor(255/(pmax-pmin))
    beta = pmin

    vec2 = list()

    if (s == "inv") :
        a = 1
    else :
        a = 0

    for elt in vec :
        vec2.append(a*(255-(elt-beta)*alpha)+(1-a)*(elt-beta)*alpha)

    return vec2





# Returns the vector convolution of vec*f

def conv1(vec,f) :

    l = floor((len(f)-1)/2)
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








# This function calculates the horizontal gradient of the picture

def hgrad1(vec) :

    f = [-1., 0., 1.]

    vec2 = conv1(vec,f)

    return vec2







# This function splits the spectrogram into different parts

def split1(picture,mean,margin,threshold) : # picture must be an Image object, mean must be a list, margin an integer and threshold a float (or an integer)

    if (os.path.exists("tmp/") == False) : # We create the folder if it does not exist yet
        os.mkdir('tmp')

    files = os.listdir("tmp/") # We erase any existing file in the "tmp/" folder as they are supposed to be temporary
    for f in files :
        os.remove("tmp/"+str(f))


    
    files = list()

    spectrogram = numpy.asarray(picture)

    v,h = spectrogram.shape[0],spectrogram.shape[1]


    m = 0
    for elt in mean :
        m = m + elt
    m = m/len(mean)

    analyse = list()
    analyse2 = list()
    for k in range(0,h) :
        if (mean[k] > threshold*m) : # Signal detection
            analyse.append(1)
        else :
            analyse.append(0)

        analyse2.append(0)


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
            for k in range(0,i-margin-1) :
                analyse2[h-k] = 1


    analyse = analyse2

    tmp = analyse[0]
    a = 0
    b = -1
    nb = 0
    for i in range(0,h): # We actually split the images
        if(analyse[i] == tmp and i < h-1) : # The image continue
           b+=1
        else : # The image changes
            b+=1
            pic = Image.fromarray(spectrogram[0:v:1,a:b:1],'RGB')
            name = "tmp/"+"0"*(3-len(str(nb)))+str(nb)
            if(analyse[i] == 1 or i == h-1) :
                name += "_silence.jpg"
            else :
                name += "_signal.jpg"
            nb+=1
            tmp = analyse[i]
            a = b
            pic.save(name)
            files.append(name)

    return files







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

def main(filename,margin,threshold,gui) :

    dimh = 0;
    dimv = 0;

    print("\nOpening "+str(filename)+"...\n")
    printC("\n",gui)
    printC("Opening "+str(filename)+"...\n",gui)

    spectrogram = openf(filename)

    print("Optimizing the spectrogram...\n")
    printC("Optimizing the spectrogram...\n",gui)
    
    spectrogram2 = BW(spectrogram)
    spectrogram2 = numpy.asarray(spectrogram2)
    spec = vec(spectrogram2)
    spec = norm1(spec,"inv")
    spec = denoise1(spec)
    #print(spec)

    print("Detecting signals...\n")
    printC("Detecting signals...\n",gui)
    
    files = split1(spectrogram, spec, margin, threshold)

    print("Optimizing signals...\n")
    printC("Optimizing signals...\n",gui)

    padding(files,dimh,dimv)

    print("Closing "+str(filename)+"...\n")
    printC("Closing "+str(filename)+"...\n",gui)

    closef(spectrogram)

    print("Done.\n")
    printC("Done.\n",gui)

    return



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


