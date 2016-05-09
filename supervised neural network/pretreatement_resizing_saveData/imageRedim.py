__author__ = 'yxu01'
import os

from PIL import Image

from lire_fichier import lire_fichier


fichiers = lire_fichier("D:\BD_images\BLU_SIGNAL\TestSet_BLU\APPRENTI")
i = 0
for [dossier,nom] in fichiers :
    print nom
    if nom.find('info') == -1:
        basewidth = 50
        img = Image.open(os.path.join(dossier,nom))
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        k = img.resize((basewidth,hsize),Image.ANTIALIAS)
        i = i+1
        s = "Resized_"+str(i)+"_"
        s=s+nom
        k.save(os.path.join(dossier,s))


