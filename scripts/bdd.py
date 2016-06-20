# -*- coding: utf-8 -*-


# This script aims at simplifying the consruction of the database


# Files must be names as follows: Modulation_ID_Frequency_Environment.Format
# Example: FM_04_103.5MHz_UrF.jpg

# Modulation must be one element of the modulations list
# ID is a natural integer linked to the modulation type (each type has its own separate counter)
# Frequency is the central frequency of the reccord with the unity (one element of the unity list)
# Environment describes the conditions by concatenating two elements of two distinct lists: one from the env list and one from the receiv list


# At the moment, one should use this script with the following command line : python bdd2.py <folderToExplore> <folderToStore> <modulation> <ID>

# which means that the folder to explore should contain only one type of modulation
# ID is a natural integer that is linked to the modulation type, ie if it is a new modulation type, the ID should be reset to 0


import os,sys,re
from math import floor
from shutil import copyfile as cp


#modulation = ["FM","AM","BLU","FSK","ASK","OFDM"]
#unity = ["Hz","kHz","MHz","GHz"]
#env = ["Me","Mo","Ru","Ur"]
#receiv = ["F","M","A"]


def main(path,folder,modulation,ID) : # Explore all files contains in this folder and its subfolders and save them under the right name in the specified folder

    #pattern = re.compile(r"*"+re.escape(modulation.lower())+r"*")


    if (os.path.exists(path) and os.path.exists(folder)) :
        files = os.listdir(path)
        for elt in files :
            if os.path.isfile(path+"/"+elt) : # treat this file
                print("ELT",elt)
                
                if not (elt.endswith(".jpg") or elt.endswith(".bmp") or elt.endswith(".png") or elt.endswith(".wav") or elt.endswith(".iq") or elt.endswith(".data")) :
                    print("Unsupported format - Error.\n")
                    next

                elif elt[:9] == "info_freq":
                    print("Unsupported file because of axis - Error.\n")
                    next

                elif  re.match(r"(\w)*"+re.escape(modulation.lower())+"(\w)*",elt.lower()) is None :
                    print("Wrong modulation type: ignoring file - Error.\n")
                    next

                else :

                    name = str(modulation) # Start with the modulation information

                    ID+=1
                    name += "_"+"0"*(6-len(str(ID)))+str(ID) # Complete with updated ID

                    
                    freq = elt.split("_")
                    try :
                        freq = int(freq[0])
                        #print("Alright",freq)
                    except ValueError :
                        freq = "X"*4
                        u = "Hz"
                        print("Name format unknown - Error.\n")

                    if freq != "X"*4 :

                        if floor(freq/10**3) == 0 :
                            u = "Hz"
                        elif floor(freq/10**6) == 0 :
                            freq = floor(freq/10**3)
                            u = "kHz"
                        elif floor(freq/10**9) == 0 :
                            freq = floor(freq/10**6)
                            u = "MHz"
                        elif floor(freq/10**12) == 0 :
                            freq = floor(freq/10**9)
                            u = "GHz"
                        elif floor(freq/10**15) == 0 :
                            freq = floor(freq/10**12)
                            u = "THz"
                        else :
                            print("Unknown frequency - Error.\n")
                            next

                    name += "_"+str(freq)+u

                    E = path.split("/")
                    E = E[len(E)-1]
                    E = E.split("_") # We get environment description

                    if len(E) == 2 :

                        R = E[1]
                        E = E[0]

                        if E == "Mer" :
                            name += "_Me"
                        elif E == "Montagne" :
                            name += "_Mo"
                        elif E == "Rural" :
                            name += "_Ru"
                        elif E == "Urbain" :
                            name += "_Ur"
                        else :
                            print("Unknown environment - Error.\n")
                            next

                        if R == "Fixe" :
                            name += "F"
                        elif R == "Mobile" :
                            name += "M"
                        elif R == "Aerien" :
                            name += "A"
                        else :
                            print("Unknown receiver type - Error.\n")
                            next

                    else :
                        name += "_XxX"
                        print("Name format unknown - Error.\n")


                    F = elt.split(".") # And the format of the file
                    F = F[len(F)-1]
                    name += "."+F

                    cp(os.path.abspath(path)+"/"+elt,os.path.abspath(folder)+"/"+name) # Copying the file to the save folder with the new name
                    print("Renamed "+name+"\n")


            elif os.path.isdir(path+"/"+elt) : # explore this folder
                print("Exploring "+elt+"...")
                ID = main(path+"/"+elt,folder,modulation,ID)

    else :
        print("Wrong path - Error.\n")
        #sys.exit()

    return ID


if __name__ == "__main__" :
    if len(sys.argv) == 5 :
        main(sys.argv[1],sys.argv[2],str(sys.argv[3]),int(sys.argv[4]))
    else :
        print("Input argument missing - Fatal Error.\n")
        sys.exit()

