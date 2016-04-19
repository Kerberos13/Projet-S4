__author__ = 'yxu01'
import dataset_GENER
from prediction import shared_dataset,predict
import cPickle
import gzip
from deep_learning_test1 import LeNetConvPoolLayer
import theano
import numpy as np


imageAdd = raw_input("plese enter image address :")
picture = dataset_GENER.openf(imageAdd)
dataset_GENER.saveData(picture)

print "Predicting image's class..."

dataAdd = raw_input("please enter trainning results data address :")
if dataAdd == "":
    result = predict('./single_image.pkl.gz',500)
else:
    result = predict(dataAdd,'./single_image.pkl.gz',500)
print (result)

