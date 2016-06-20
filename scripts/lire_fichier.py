__author__ = 'yxu01'
import os
def lire_fichier(NomfichierS) :
    NomfichierD =[]
    for dossier,sous_dossier,fichiers in os.walk(NomfichierS):
        for fichier in fichiers :
            NomfichierD.append([dossier,fichier])
    return NomfichierD