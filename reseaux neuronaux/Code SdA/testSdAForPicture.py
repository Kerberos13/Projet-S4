# -*- coding: utf-8 -*-
"""
Created on Mon May 16 18:15:05 2016

@author: Jingei SHI
"""

import os
import cPickle
import numpy
import theano
import theano.tensor as T
from PIL import Image
from lire_fichier import lire_fichier


class HiddenLayer(object):
    def __init__(self, input, params_W, params_b,
                 activation=T.tanh):
        self.input = input
        self.W = params_W
        self.b = params_b

        lin_output = T.dot(input, self.W) + self.b
        self.output = (
            lin_output if activation is None
            else activation(lin_output)
        )
        self.params = [self.W, self.b]


class LogisticRegression(object):
    def __init__(self, input, params_W, params_b, n_in, n_out):
        self.W = params_W
        print self.W.size
        self.b = params_b
        print self.b.size
        self.p_y_given_x = T.nnet.softmax(T.dot(input, self.W) + self.b)
        self.y_pred = T.argmax(self.p_y_given_x, axis=1)
        self.params = [self.W, self.b]

    def negative_log_likelihood(self, y):
        return -T.mean(T.log(self.p_y_given_x)[T.arange(y.shape[0]), y])

    def errors(self, y):
        if y.ndim != self.y_pred.ndim:
            raise TypeError(
                'y should have the same shape as self.y_pred',
                ('y', y.type, 'y_pred', self.y_pred.type)
            )
        if y.dtype.startswith('int'):
            return T.mean(T.neq(self.y_pred, y))
        else:
            raise NotImplementedError()


def shared_dataset(data_x, borrow=True):
    """ Function that loads the dataset into shared variables

    The reason we store our dataset in shared variables is to allow
    Theano to copy it into the GPU memory (when code is run on GPU).
    Since copying data into the GPU is slow, copying a minibatch everytime
    is needed (the default behaviour if the data is not in a shared
    variable) would lead to a large decrease in performance.
    """

    shared_x = theano.shared(numpy.asarray(data_x,
                                           dtype=theano.config.floatX),
                             borrow=borrow)
    # When storing data on the GPU it has to be stored as floats
    # therefore we will store the labels as ``floatX`` as well
    # (``shared_y`` does exactly that). But during our computations
    # we need them as ints (we use labels as index, and if they are
    # floats it doesn't make sense) therefore instead of returning
    # ``shared_y`` we will have to cast it to int. This little hack
    # lets ous get around this issue
    return shared_x


def BW(picture):
    if isinstance(picture, Image.Image):  # We verify that we effectively are working on an Image object
        picture = picture.convert('L')
        return picture


def load_params(params_file):
    f = open(params_file, 'rb')
    params = cPickle.load(f)
    f.close()

    return params


def load_data(dataset_path):
    fichiers = lire_fichier(dataset_path)
    images_arrary = numpy.empty((len(fichiers), 1850), dtype='float32')
    i = 0
    for [dossier, nom] in fichiers:
        # resize to 50*37
        if nom.find('info') == -1:
            basewidth = 50
            img = Image.open(os.path.join(dossier, nom))
            #wpercent = (basewidth / float(img.size[0]))
            # hsize = int((float(img.size[1])*float(wpercent)))
            hsize = 37
            bw_image = img.resize((basewidth, hsize), Image.ANTIALIAS)

            # pretreatement of images
            # bw_image = BW(k)
            bw_image = numpy.asarray(bw_image, dtype='float32')
            bw_image = bw_image / 255
            bw_image = bw_image.flatten()
            images_arrary[i] = bw_image
            i = i + 1
            # copy each row to fit the batch_size
    return shared_dataset(images_arrary)



def test_SdAForPicture(
        dataset=r'C:\Users\Administrator\Desktop\SNR2\SNR test\BLU\30dB',
        params_file=r'E:\TB DAYS\S4\projetS4 Jinglei\parametres\parametres\autoencoder\params_BdV2.5_SDA_mix_50_37_BW_compatible.pkl'):
    faces = load_data(dataset)

    # load data
    params = load_params(params_file)     # load the parameters of the neuronal network.
    w1 = params[0]
    b1 = params[1]
    w2 = params[2]
    b2 = params[3]
    w3 = params[4]
    b3 = params[5]
    x = T.matrix('x')

    ######################
    # initialization
    ######################
    '''The constructure of a neuronal network: two hidden layers and a layer of classification'''
    layer0 = HiddenLayer(
        input=x,
        params_W=w1,
        params_b=b1,
        activation=T.nnet.sigmoid)

    layer1 = HiddenLayer(
        input=layer0.output,
        params_W=w2,
        params_b=b2,
        activation=T.nnet.sigmoid)

    layer2 = LogisticRegression(input=layer1.output, params_W=w3, params_b=b3
                                , n_in=1000, n_out=5)

    f = theano.function(
        [x],
        layer2.y_pred
    )

    # list of prediction result in numbers, please check label_number.txt for number info for each type
    """
    output:
    pred: a
    AM -> 0
    FM -> 1
    FSK -> 2
    ASK -> 3
    BLU -> 4
    """
    inputs = numpy.asanyarray(faces.get_value(borrow=True), dtype=theano.config.floatX)
    pred = f(inputs)
    #Calculate error rate of each modulation.
    y0 = numpy.zeros(pred.shape, dtype="float32") + 0.
    error_rate = numpy.mean(pred == y0)
    print 'AM:',error_rate * 100.
    
    y1 = numpy.zeros(pred.shape, dtype="float32") + 1.
    error_rate = numpy.mean(pred == y1)
    print 'FM:',error_rate * 100.

    y2 = numpy.zeros(pred.shape, dtype="float32") +2.
    error_rate = numpy.mean(pred == y2)
    print 'FSK:',error_rate * 100.
    
    y3 = numpy.zeros(pred.shape, dtype="float32") +3.
    error_rate = numpy.mean(pred == y3)
    print 'ASK:',error_rate * 100.
    
    y4 = numpy.zeros(pred.shape, dtype="float32") +4.
    error_rate = numpy.mean(pred == y4)
    print 'BLU:',error_rate * 100.

if __name__ == '__main__':
    test_SdAForPicture()
