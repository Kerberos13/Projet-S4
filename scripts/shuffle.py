# -*- coding: utf-8 -*-


# This script aims at simplifying the consruction of the database
# It creates three folders filled with randomly picked files according to some percentages

# It should be launched with the following command line: python shuffle.py <FolderToExplore'sPath> <TrainingSetPercentage> <TestingSetPercentage> <ValidationSetPercentage> 


import os,sys
from math import floor
from shutil import copyfile as cp
from random import shuffle



def main(folderToExplore,TrainPerc,TestPerc,ValidPerc) :

    if os.path.exists(folderToExplore) :

        if float(TrainPerc)+float(TestPerc)+float(ValidPerc) != float(1.0) :
            print("Wrong Percentages - Fatal Error.\n")
            sys.exit()
            return

        TrainFolder = folderToExplore+"Entrainement/"
        TestFolder = folderToExplore+"Test/"
        ValidFolder = folderToExplore+"Validation/"


        for elt in [TrainFolder,TestFolder,ValidFolder] :

            if not os.path.exists(elt) :
                os.mkdir(elt)
            


        files = os.listdir(folderToExplore)
        files2 = list()
        for elt in files :
            if len(elt) != 0 and (elt.endswith(".bmp") or elt.endswith(".jpg")):
                files2.append(elt)


        nbTraining = floor(float(TrainPerc)*len(files2))
        nbTest = floor(float(TestPerc)*len(files2))
        nbValidation = len(files2) - (nbTraining + nbTest)


        #treated = list()

        treated = 0
        indexes = list(range(0,len(files2)))
        shuffle(indexes)


        for k in range(0,3) :

            if k == 0 :
                N = nbTraining
                Folder = TrainFolder
            if k == 1 :
                N = nbTraining + nbTest
                Folder = TestFolder
            if k == 2 :
                N = nbTraining + nbTest + nbValidation
                Folder = ValidFolder

            """
            while len(treated) < N :
                
                TREATED = False
                i = randint(0,len(files2)-1)
                for elt in treated :
                    if elt == i :
                        TREATED = True

                while TREATED == True :
                    TREATED = False
                    i = randint(0,len(files2)-1)
                    for elt in treated :
                        if elt == i :
                            TREATED = True
               
                #print(i)

                cp(folderToExplore+"/"+files2[i],Folder+files2[i])

                treated.append(i)

                print(str(len(treated))+"/"+str(len(files2)))
                """            
                
            #treated = 0
            while (treated < N and len(indexes) != 0) :
                
                i = indexes.pop()
                cp(folderToExplore+"/"+files2[i],Folder+files2[i])
                treated += 1

                print(str(treated)+"/"+str(len(files2)))

    else :
        print("Wrong Path - Fatal Error.\n")
        sys.exit()

    return



if __name__ == "__main__" :
    if len(sys.argv) == 5 :
        main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    else :
        print("Input argument missing - Fatal Error.\n")
        sys.exit()

