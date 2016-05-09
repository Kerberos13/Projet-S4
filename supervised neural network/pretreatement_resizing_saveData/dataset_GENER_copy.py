__author__ = 'yxu01'
import sys
import os
import cPickle

import numpy
from PIL import Image

from lire_fichier import lire_fichier

#fuction copyed from sign_detect2, Benoit
def openf(fileName) :

    if (os.path.exists(fileName)) : # We verify that the path is correct,
        thumbnail = Image.open(fileName)
        return thumbnail

    else :
        print("Incorrect Path - Fatal Error.\n")
        sys.exit()
        return

def BW(picture) :
    if isinstance(picture,Image.Image) : # We verify that we effectively are working on an Image object
        picture = picture.convert('L')
        return picture

def HSV(picture) :
    if isinstance(picture,Image.Image) : # We verify that we effectively are working on an Image object
        picture = picture.convert('HSV')
        h = picture.shape[0]
        v = picture.shape[1]
        picture = picture[0:h,0:v,0]
        return picture

    else :
        print("Wrong Type - Fatal Error.\n")
        sys.exit()
        return

def saveData(imageAd,fileName="./Bd_signaux_client.pkl.gz"):
    sets=[]
    for k in range(len(imageAd)):
        fichiers = lire_fichier(imageAd[k])
        i = 0
        out = numpy.asarray([],dtype='float32')
        labelNum = []
        while i < len(fichiers) :
            image = openf(os.path.join(fichiers[i][0],fichiers[i][1]))
            bw_image = BW(image)
            width, height = bw_image.size
            if width ==50 and height == 37:
                bw_image = numpy.asarray(bw_image,dtype='float32')
                print(bw_image.shape)
                bw_image = bw_image/255
                bw_image = bw_image.flatten()


                if int(out.shape[0]) == 0 :
                    out = bw_image #first image
                    #define label according to signal modulation type
                    if (fichiers[i][1].find('AM')>= 0):
                        labelNum.append(0)
                    if (fichiers[i][1].find('FM')>= 0) :
                        labelNum.append(1)
                    if (fichiers[i][1].find('FSK')>= 0):
                        labelNum.append(2)
                    if (fichiers[i][1].find('ASK')>= 0) :
                        labelNum.append(3)
                    if (fichiers[i][1].find('BLU')>= 0) :
                        labelNum.append(4)
                else:
                    out = numpy.vstack((out,bw_image)) #add new image to a row
                    if (fichiers[i][1].find('AM')>= 0) and len(labelNum) == (int(out.shape[0])-1) :
                        labelNum.append(0)
                    if (fichiers[i][1].find('FM')>= 0) and len(labelNum) == (int(out.shape[0])-1):
                        labelNum.append(1)
                    if (fichiers[i][1].find('FSK')>= 0) and len(labelNum) == (int(out.shape[0])-1):
                        labelNum.append(2)
                    if (fichiers[i][1].find('ASK')>= 0) and len(labelNum) == (int(out.shape[0])-1):
                        labelNum.append(3)
                    if (fichiers[i][1].find('BLU')>= 0) and len(labelNum) == (int(out.shape[0])-1):
                        labelNum.append(4)

            i= i+1

        label = numpy.asarray(labelNum,dtype='int16')
        sets.append([out,label])
#        with gzip.open("./set_"+str(k)+".pkl.gz", 'wb') as f1:
        f1 = open("./set_"+str(k)+"_50-37_mymixed_5types_BW"+".save", 'wb')
        cPickle.dump([sets[k]], f1,protocol=cPickle.HIGHEST_PROTOCOL)
        f1.close()

    f = open("Bd_signaux_client_50_37_mixed_5_types_BW.save", 'wb')
    cPickle.dump([sets[0],sets[1],sets[2]], f,protocol=cPickle.HIGHEST_PROTOCOL)
    f.close()
    # with gzip.open(fileName, 'wb') as f:
    #     cPickle.dump([sets[0],sets[1],sets[2]], f)
    return 0


