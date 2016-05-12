# -*- coding: utf-8 -*-


# This script aims at simplifying the consruction of the database
# This script analyses all pictures in a folder and removes all redundant pictures (ie if exact double)


# At the moment, one should use this script with the following command line : python NoDouble.py folderToExplore

import os,sys,numpy
from PIL import Image




def main(folder) :

    if os.path.exists(folder) :

        files = os.listdir(folder)
        
        offset = 5933
        i = offset
        for elt in files[offset:] :
            if elt.endswith(".jpg") : # We can analyse this picture
                
                if os.path.exists(folder+"/"+elt) :

                    print(str(i)+"/"+str(len(files)))
                    img1 = Image.open(folder+"/"+elt)

                    for el in files[i+1:] : # The rest of the pictures
                        
                        if os.path.exists(folder+"/"+el) and el.endswith(".jpg"):
                            
                            img2 = Image.open(folder+"/"+el)

                            # If we arrive at this point, this means that we have successfully opened img1 and img2. We can now compare them

                            #img1 = img # We make a copy of the first image since we might resize it

                            # We ensure that the two images have the same dimensions

                            W1,H1 = img1.size[0],img1.size[1]
                            W2,H2 = img2.size[0],img2.size[1]

                            """
                            if W1 < W2 :
                                img2.resize((W1,H2),Image.ANTIALIAS)
                            elif W1 > W2 :
                                img1.resize((W2,H2),Image.ANTIALIAS)

                            if H1 < H2 :
                                img2.resize((W2,H1),Image.ANTIALIAS)
                            elif H1 > H2 :
                                img1.resize((W1,H2),Image.ANTIALIAS)
                            """

                            if (W1 == W2 and H1 == H2) :

                                # We convert them into matrices

                                pic1 = numpy.asarray(img1)
                                pic2 = numpy.asarray(img2)

                                img2.close()

                                # And we compare them pixel by pixel

                                diff = abs(pic2-pic1)
                                diff = numpy.sum(diff,(0,1,2))

                                #print(diff)

                                if diff == 0 : # Since the sum of all pixel-to-pixel differences is null, we have exact doubles
                                    os.remove(folder+"/"+el) # we delete the second picture
                                    print("Exact double detected bewteen "+elt+" and "+el+": "+el+" removed.")
                                
                        else :
                            next

                    img1.close()
                else :
                    next

                i+=1
                #print(elt)

        else :
            print("Unsupported file format - Error.\n")
            next


    else :
        print("Wrong Path - Fatal Error.\n")
        sys.exit()

    return




if __name__ == "__main__" :
    if len(sys.argv) == 2 :
        main(sys.argv[1])
    else :
        print("Input argument missing - Fatal Error.\n")
        sys.exit()



