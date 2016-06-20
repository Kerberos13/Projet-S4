# -*-coding:utf8-*-#
__author__ = 'G52 ProjetS4'
"""
Fonction interne
ce code est utilisé pour rendre la matrice de l'ordre aléatoire.

    :type array : .save (numpy.ndarray float32)
    :param array : matrice (nombre des signaux * taille d'un signal) des signaux compréssée sous forme ".save".
                   taille d'un signal = nombre de pixels d'un spectrogramme(ici 50*37 =1850)

    :type labelarr : .save (numpy.ndarray int16)
    :param labelarr : vecteur des labels (nombre des signaux *1) compréssé sous forme ".save".

    :type iter : int
    :param iter : nombre d'itérations

exemple :
    signal label           signal label
     1       0              6       1
     2       0              5       1
     3       0  ----->      3       0
     4       1              1       0
     5       1              4       1
     6       1              2       0

"""
import numpy as np
def randoom_exchange (array,labelarr,iter):
    def swap_rows(arr, frm, to):
        if arr.shape == (arr.shape[0],):# si c'est un vecteur
            arr[[frm, to]] = arr[[to, frm]]
        else : #si c'est une matrice
            arr[[frm, to],:] = arr[[to, frm],:]

    for i in range(iter):
        b = np.random.randint(0,array.shape[0],2)
        swap_rows(array,b[0],b[1])
        swap_rows(labelarr,b[0],b[1])



