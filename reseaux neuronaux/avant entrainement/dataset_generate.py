# -*-coding:utf8-*-#
__author__ = 'Groupe52 ProjetS4'
import sys
import os
import pickle
import numpy
from PIL import Image

def lire_fichier(NomfichierS) :
    '''
    parcourir un dossier
    :type NomfichierS: String
    :param NomfichierS: nom du dossier source
    :return NomfichierD : liste des adresses(String) des fichiers dans le dossier
    '''
    NomfichierD =[]
    for dossier,sous_dossier,fichiers in os.walk(NomfichierS):
        for fichier in fichiers :
            NomfichierD.append([dossier,fichier])
    return NomfichierD

def openf(fileName) :

    '''
    ouvrir un fichier image (.jpeg, .bmp, .png)
    :type fileName: String
    :param fileName: nom du fichier source
    :return picture : Image class
    '''

    if (os.path.exists(fileName)) :
        picture = Image.open(fileName)
        return picture

    else :
        print("Incorrect Path - Fatal Error.\n")
        sys.exit()
        return

def BW(picture) :
    '''
    rendre un fichier image (Image class) noir et blanc
    :type fileName: Image class
    :param fileName: image
    :return picture : Image class, noir et blanc
    '''

    if isinstance(picture,Image.Image) : # We verify that we effectively are working on an Image object
        picture = picture.convert('L')
        return picture

def saveData(imageAd):
    '''
    prétraitement des images et les sauvegrader en ajoutant des labels associés
    :type imageAd: list of String
    :param imageAd: [entrainement, test, valitation]
    output : matrice (nombre des signaux * taille d'un signal) des signaux compréssée sous forme ".save".
            taille d'un signal = nombre de pixels d'un spectrogramme(ici 50*37 =1850)
    '''
    sets=[]
    for k in range(len(imageAd)):
        fichiers = lire_fichier(imageAd[k])
        i = 0
        out = numpy.asarray([],dtype='float32')
        labelNum = []
        while i < len(fichiers) :
            bw_image = openf(os.path.join(fichiers[i][0],fichiers[i][1]))
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

    f = open("BdV2.5_fatices_50_37_BW.save", 'wb')
    #sets[0] training dataset; sets[1] test dataset dataset; sets[2] validation dataset
    pickle.dump([sets[0],sets[1],sets[2]], f)
    f.close()
    return 0

if __name__ == '__main__':
    imageAdd = [];
    imageAdd.append(raw_input("plese enter TrainingSet address :"))
    imageAdd.append(raw_input("plese enter TestSet address:"))
    imageAdd.append(raw_input("plese enter ValidationSet address:"))
    saveData(imageAdd)
