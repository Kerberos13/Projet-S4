# -*-coding:utf8-*-#

import os,sys
try :
    import pickle
except ImportError :
    import pickle as pickle

sys.path.insert(0,'scripts/')

#import pickle
from lire_fichier import lire_fichier

import numpy
from PIL import Image

import theano
import theano.tensor as T
from theano.tensor.signal import downsample
from theano.tensor.nnet import conv
def BW(picture) :
    if isinstance(picture,Image.Image) : # We verify that we effectively are working on an Image object
        picture = picture.convert('L')
        return picture

def load_params(params_file):
    f=open(params_file,'rb')
    params=pickle.load(f)
    f.close()
    return params


#read image(s) et resized them
def load_data(dataset_path):
    fichiers = lire_fichier(dataset_path)
    print(fichiers)
    images_arrary = numpy.empty((len(fichiers),1850),dtype='float32')
    i=0
    for [dossier,nom] in fichiers :
        #resize to 50*37
        if nom.find('info') == -1:
            basewidth = 50
            img = Image.open(os.path.join(dossier,nom))
            wpercent = (basewidth/float(img.size[0]))
            #hsize = int((float(img.size[1])*float(wpercent)))
            hsize = 37
            k = img.resize((basewidth,hsize),Image.ANTIALIAS)

            #pretreatement of images
            bw_image = BW(k)
            bw_image = numpy.asarray(bw_image,dtype='float32')
            bw_image = bw_image/256.
            bw_image = bw_image.flatten()
            images_arrary[i]=bw_image
            i=i+1
            #copy each row to fit the batch_size
    return images_arrary





"""
prediction
"""
class LogisticRegression(object):
    def __init__(self, input, params_W,params_b,n_in, n_out):
        self.W = params_W
        self.b = params_b
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


class HiddenLayer(object):
    def __init__(self, input, params_W,params_b, n_in, n_out,
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

	
#（conv+maxpooling）
class LeNetConvPoolLayer(object):
    def __init__(self,  input,params_W,params_b, filter_shape, image_shape, poolsize=(2, 2)):
        assert image_shape[1] == filter_shape[1]
        self.input = input

        self.W = params_W

        self.b = params_b
        # conv
        conv_out = conv.conv2d(
            input=self.input,
            filters=self.W,
            filter_shape=filter_shape,
            image_shape=image_shape
        )
        # maxpooling
        pooled_out = downsample.max_pool_2d(
            input=conv_out,
            ds=poolsize,
            ignore_border=True
        )
        self.output = T.tanh(pooled_out + self.b.dimshuffle('x', 0, 'x', 'x'))
        self.params = [self.W, self.b]


"""
n_kerns should be the same as tranning.
input :
    param dataMatrix :
        type : numpy.ndarray, dtype="float32"
        format : !!each row is a flattened BW normalized(ie./256) image (50*37=1850),
                 to transform oringinal image like this, please reference function
                 load_data in this file use_CNN.py

    param_file : address of the trained paramters(by default, should be in the same repertory)
    nkerns : please not change

output :
    pred : a list with the labels
    type : int32
    label table :
           AM -> 0
           FM -> 1
           FSK -> 2
           ASK -> 3
           BLU -> 4
PS: please note that this funtion use all the classes defined in the file, pay attention when import.
"""
def use_CNN(dataMatrix,params_file='scripts/params_BdV2.5_mixed_50_37_BW_compatible.pkl',nkerns=[10, 15]):#'scripts/params_mixed_5types_CPU.pkl'

    #read param.pkl
    #layer0_params~layer3_params with w,b data,layer*_params[0] is data W，layer*_params[1] is data b
    def load_params(params_file):
        f=open(params_file,'rb')

        if int(sys.version[0]) == 2 :
            params=pickle.load(f)
            
        elif int(sys.version[0]) == 3 :
            params=pickle.load(f,encoding='latin1')
        
        else :
            print("Unsupported version of python: please upgrade to Python 2.7 or greater - Fatal Error.")
            sys.exit()



        #params=pickle.load(f)
        f.close()
        return params

    dataMatrix_num = dataMatrix.shape[0]
  
    #load data
    params=load_params(params_file)
    layer0_W =params[0]
    layer0_b =params[1]
    layer1_W =params[2]
    layer1_b =params[3]
    layer2_W =params[4]
    layer2_b =params[5]
    layer3_W =params[6]
    layer3_b =params[7]

    #print("type param")
    x = T.matrix('x',dtype="float32")

    ######################
    #initialization
    ######################
    layer0_input = x.reshape((dataMatrix_num, 1, 37, 50))
    layer0 = LeNetConvPoolLayer(
        input=layer0_input,
        params_W=layer0_W,
        params_b=layer0_b,
        image_shape=(dataMatrix_num, 1, 37, 50),
        filter_shape=(nkerns[0], 1, 5, 5),
        poolsize=(2, 2)
    )

    layer1 = LeNetConvPoolLayer(
        input=layer0.output,
        params_W=layer1_W,
        params_b=layer1_b,
        image_shape=(dataMatrix_num, nkerns[0], 16, 23),
        filter_shape=(nkerns[1], nkerns[0], 5, 5),
        poolsize=(2, 2)
    )

    layer2_input = layer1.output.flatten(2)
    layer2 = HiddenLayer(
        input=layer2_input,
        params_W=layer2_W,
        params_b=layer2_b,
        n_in=nkerns[1] * 6 * 9,
        n_out=2500,
        activation=T.tanh
    )

    layer3 = LogisticRegression(input=layer2.output, params_W=layer3_W,params_b=layer3_b
                                ,n_in=2500, n_out=5)
     

    f = theano.function(
        [x],
        layer3.y_pred
    )
    #print(type(dataMatrix))
    pred = f(dataMatrix)
    pred=numpy.asarray(pred,dtype="int32")
    return pred.tolist()


