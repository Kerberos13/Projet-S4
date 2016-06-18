# -*- coding: utf-8 -*-

# The aim of this module is to provide generic tools for different modules

import sys, os, numpy, time
from PIL import Image
from math import floor



# This is a mutex, a shared resource with mutual exclusion in order to avoid conflict

class mutex() :

    def __init__(self,value) :
        self.content = value
        self.locked = False
        return

    def set(self,value) :
        if self.lock() :
            self.content = value
            self.unlock()
        return

    def get(self) :
        if self.lock() :
            content = self.content
            self.unlock()
        else :
            content = None
        return content

    def lock(self) :
        i = 0
        while (i<10) : # We allow up to 10 tries
            if self.locked : # The lock has already been taken
                i+=1
                time.sleep(.1)
            else : # The lock is free
                self.locked = True
                return True # Locking was a success
        return False # Locking was a failure

    def unlock(self) :
        self.locked = False
        return



# This function opens an existing spectrogram

def openf(fileName) :

    if (os.path.exists(fileName)) : # We verify that the path is correct
        spectrogram = Image.open(fileName)
        spectrogram = spectrogram.convert('RGB')
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
        picture = numpy.asarray(picture)
        h,v = picture.shape[0],picture.shape[1]
        #picture = (picture[0:h,0:v,0]*1+picture[0:h,0:v,1]*1+picture[0:h,0:v,2]*4)/6
        return picture

    else :
        print("Wrong Type - Fatal Error.\n")
        sys.exit()
        return



# This function makes an RGB picture into a Hue Saturation Value Picture

def HSV(picture) :
    
    if isinstance(picture,Image.Image) : 
        picture = picture.convert('HSV')
        picture = numpy.asarray(picture)
        h,v = picture.shape[0],picture.shape[1]
        picture = picture[0:h,0:v,0]

        return picture

    else :
        print("Wrong Type - Fatal Error.\n")
        sys.exit()
        return



# This function normalises the pixels' value from 0 to 170 from a numpy array (Hue component of a HSV diagram)

def norm2HSV(picture) :

    isArray = isinstance(picture,numpy.ndarray)

    if isArray : # We verify that we effectively are working on an Image object

        picture = numpy.asarray(picture)
        picture.flags.writeable = True # This makes the picture writeable and not read-only
        h,v = picture.shape[0],picture.shape[1] # We get the dimensions of the picture: horizontaly and verticaly
        
        pmin = numpy.amin(picture,(0,1))
        pmax = numpy.amax(picture,(0,1))
        #print(pmin,pmax)

        picture = pmin + pmax - picture # We invert the values

        if pmax == pmin :
            print("Empty image - Error.\n")

        elif(pmin != 0 and pmax != 170) :
            alpha = 170/(pmax-pmin)
            beta = 0-alpha*pmin
            #print(alpha,beta)

            picture = picture*alpha + beta
            picture = numpy.floor(picture)
            pmin = numpy.amin(picture,(0,1))
            pmax = numpy.amax(picture,(0,1))
            #print(pmin,pmax)

        return picture

    else :
        print("Wrong Type - Fatal Error.\n")
        sys.exit()
        return


# This function normalises the pixels' value from 0 to 255 from a picture

def norm2(picture) :

    isPic = isinstance(picture,Image.Image)
    isArray = isinstance(picture,numpy.ndarray)

    if isPic or isArray : # We verify that we effectively are working on an Image object

        picture = numpy.asarray(picture)
        picture.flags.writeable = True # This makes the picture writeable and not read-only
        h,v = picture.shape[0],picture.shape[1] # We get the dimensions of the picture: horizontaly and verticaly


        """ 
        pmin = 255
        pmax = 0


        for i in range(0,h-1) : # We look for the minimum and maximum pixel value
            for j in range(0,v-1) :
                if (picture[i,j] <= pmin) :
                    pmin = picture[i,j]
                if (picture[i,j] >= pmax) :
                    pmax = picture[i,j]
        """
        pmin = numpy.amin(picture,(0,1))
        pmax = numpy.amax(picture,(0,1))
        #print(pmin,pmax)

        if pmax == pmin :
            print("Empty image - Error.\n")


        elif(pmin != 0 and pmax != 255) :
            alpha = 255/(pmax-pmin)
            beta = 0-alpha*pmin
            #print(alpha,beta)
            
            #picture1=numpy.asarray(picture)

            for i in range(0,h) : # And we adjust them to improve overall contrast for edge detection
                for j in range(0,v) :
                    picture[i,j] = int(floor(picture[i,j]*alpha+beta))
                    #picture1[i,j] = int(floor(picture1[i,j]*alpha+beta))
            

            #picture2 = numpy.floor(picture*alpha + beta)
            #picture2 = numpy.asarray(picture2,dtype=numpy.uint)

            #pmin = numpy.amin(picture2,(0,1))
            #pmax = numpy.amax(picture2,(0,1))
            #print("NORM2",pmin,pmax)
            #print(picture2)
            #print(picture1)
            #print(numpy.abs(picture2-picture1))

            #print(numpy.sum(numpy.abs(picture2-picture1)))

            if isPic :
                picture = Image.fromarray(picture,'L')
        
        return picture

    else :
        print("Wrong Type - Fatal Error.\n")
        sys.exit()
        return



# This functions normalizes the pixels' value of a picture, from 0 to 255 using a log function

def norm2log(picture) :


    isPic = isinstance(picture,Image.Image)
    isArray = isinstance(picture,numpy.ndarray)

    if isPic or isArray : # We verify that we effectively are working on an Image object

        picture = numpy.asarray(picture)
        picture.flags.writeable = True # This makes the picture writeable and not read-only
        h,v = picture.shape[0],picture.shape[1] # We get the dimensions of the picture: horizontaly and verticaly

        pmin = numpy.amin(picture,(0,1))
        pmax = numpy.amax(picture,(0,1))
        #print(pmin,pmax)

        if pmax == pmin :
            print("Empty image - Error.\n")


        elif(pmin != 0 and pmax != 255) :
            picture = numpy.log((picture+pmin+1))
            pmin = numpy.amin(picture,(0,1))
            pmax = numpy.amax(picture,(0,1))
                
            alpha = 255/(pmax-pmin)
            beta = 0-alpha*pmin
            #print(alpha,beta)


            picture = numpy.floor(picture*alpha + beta)
            #pmin = numpy.amin(picture,(0,1))
            #pmax = numpy.amax(picture,(0,1))
            #print(pmin,pmax)

            if isPic :
                picture = Image.fromarray(picture,'L')
        
    return picture



# This functions normalizes the pixels' value from 0 to 255 from a list

def norm1(vec,s) :

    #print(vec)

    pmin = min(vec)
    pmax = max(vec)

    if pmin == pmax :
        print("Empty image - Error.\n")
        vec2 = vec

    elif ((pmax != 255 or pmin != 0) or (s=="inv")) :
        alpha = floor(255/(pmax-pmin))
        beta = 0-alpha*pmin

        vec2 = list()

        if (s == "inv") :
            a = 1
        else :
            a = 0

        for elt in vec :
            vec2.append(a*(255-(elt*alpha+beta))+(1-a)*(elt*alpha+beta))

    else :
        vec2 = vec

    return vec2



# This functions does zero padding to a given picture (NxMx1 matrix)

def padding1(pic,dimh,dimv) :
    
    v,h = pic.shape[0],pic.shape[1]

    if (h < dimh) : # The picture is currently not wide enough
        a = dimh - h
        b = floor(a/2)
        a = a - b

        col = numpy.zeros((v,1,1),dtype=pic.dtype)

        for i in range(0,a) :
            pic = numpy.concatenate((col,pic),axis=1)

        for i in range(0,b) :
            pic = numpy.concatenate((pic,col),axis=1)

    if (v < dimv) : # The picture is currently not long enough
        a = dimv - v
        b = floor(a/2)
        a = a - b

        row = numpy.zeros((1,h,1),dtype=pic.dtype)

        for i in range(0,a) :
            pic = numpy.concatenate((row,pic),axis=0)

        for i in range(0,b) :
            pic = numpy.concatenate((pic,row),axis=0)

    return pic

    # Note: we do not do anything if the picture is too big. The crop will have to be handled by the second module.




# This functions does zero padding to a given picture (RGB or HSVi NxMx3 matrix)

def padding3(pic,dimh,dimv) :
    
    v,h = pic.shape[0],pic.shape[1]

    if (h < dimh) : # The picture is currently not wide enough
        a = dimh - h
        b = int(floor(a/2))
        a = int(a - b)

        col = numpy.zeros((v,1,3),dtype=pic.dtype)

        for i in range(0,a) :
            pic = numpy.concatenate((col,pic),axis=1)

        for i in range(0,b) :
            pic = numpy.concatenate((pic,col),axis=1)

    if (v < dimv) : # The picture is currently not long enough
        a = dimv - v
        b = int(floor(a/2))
        a = int(a - b)

        row = numpy.zeros((1,h,3),dtype=pic.dtype)

        for i in range(0,a) :
            pic = numpy.concatenate((row,pic),axis=0)

        for i in range(0,b) :
            pic = numpy.concatenate((pic,row),axis=0)

    return pic

    # Note: we do not do anything if the picture is too big. The crop will have to be handled by the second module.




# This function eliminates the possible zero-padding for a NxMx3 matrix

def unpad3(picture,margin) :

    # Because we have margins, we are sure that the signal's dimensions are greater than 1*1 pixel, and because the signal is centered when padded, it is sufficient to analyse the middle row and the middle column to unpad.

    v,h = picture.shape[0],picture.shape[1]

    a = floor(v/2)
    b = floor(h/2)

    picture2 = numpy.asarray(picture)

    for i in range(1,h+1) : # We analyse along the horizontal axis
        if numpy.array_equal(picture[a,h-i,:],[0,0,0]) : # Note: for this equality to be verified, we must use lossless compression algorithms such as bmp and not jpg
            picture2 = numpy.delete(picture2,h-i,1) # We delete the column i

    for i in range(1,v+1) : # We analyse along the vertical axis
        if numpy.array_equal(picture[v-i,b,:],[0,0,0]) :
            picture2 = numpy.delete(picture2,-i,0) # We delete the row i

    return picture2



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




# This function calculates the horizontal gradient of the picture

def hgrad1(vec) :

    f = [-1., 0., 1.]

    vec2 = conv1(vec,f)

    return vec2





# This function merges the picture ndarray at the right of the pic ndarray

def merge(pic,picture) :
 
    pic = numpy.hstack((pic,picture))

    return pic









