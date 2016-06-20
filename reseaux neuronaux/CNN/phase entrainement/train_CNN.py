# -*-coding:utf8-*-#
__author__ = 'http://deeplearning.net/tutorial/lenet.html'

"""
Adopté et modifié par Groupe 52 Projet S4.
Ce code est pour entraîner le réseau CNN.
couche 1 : convolution + maxpooling
couche 2 : convolution + maxpooling
couche 3 : hidden layer
couche 4 : logistic regression (classifier)

"""
import pickle
import os
import sys
import time
import numpy
import theano
import theano.tensor as T
from theano.tensor.signal import downsample
from theano.tensor.nnet import conv
from Random_matrix import randoom_exchange

def load_data(dataset):
    '''
    Loads the dataset
    :type dataset: string
    :param dataset: the path to the dataset
    '''

    #############
    # LOAD DATA #
    #############

    data_dir, data_file = os.path.split(dataset)
    if data_dir == "" and not os.path.isfile(dataset):
        # Check if dataset is in the data directory.
        new_path = os.path.join(
            os.path.split(__file__)[0],
            "..",
            "data",
            dataset
        )
        if os.path.isfile(new_path) :
            dataset = new_path

    print '... loading data'

    # Load the dataset
    f = open(dataset, 'rb')
    train_set, test_set,valid_set= pickle.load(f)
    randoom_exchange(train_set[0],train_set[1],int(train_set[0].shape[0]/2))
    randoom_exchange(test_set[0],test_set[1],int(test_set[0].shape[0]/2))
    randoom_exchange(valid_set[0],valid_set[1],int(valid_set[0].shape[0]/2))
    f.close()
    #train_set, valid_set, test_set format: tuple(input, target)
    #input is an numpy.ndarray of 2 dimensions (a matrix)
    #witch row's correspond to an example. target is a
    #numpy.ndarray of 1 dimensions (vector)) that have the same length as
    #the number of rows in the input. It should give the target
    #target to the example with the same index in the input.

    def shared_dataset(data_xy, borrow=True):
        """ Function that loads the dataset into shared variables

        The reason we store our dataset in shared variables is to allow
        Theano to copy it into the GPU memory (when code is run on GPU).
        Since copying data into the GPU is slow, copying a minibatch everytime
        is needed (the default behaviour if the data is not in a shared
        variable) would lead to a large decrease in performance.
        """
        data_x, data_y = data_xy
        shared_x = theano.shared(numpy.asarray(data_x,
                                               dtype=theano.config.floatX),
                                 borrow=borrow)
        shared_y = theano.shared(numpy.asarray(data_y,
                                               dtype=theano.config.floatX),
                                 borrow=borrow)
        # When storing data on the GPU it has to be stored as floats
        # therefore we will store the labels as ``floatX`` as well
        # (``shared_y`` does exactly that). But during our computations
        # we need them as ints (we use labels as index, and if they are
        # floats it doesn't make sense) therefore instead of returning
        # ``shared_y`` we will have to cast it to int. This little hack
        # lets ous get around this issue
        return shared_x, T.cast(shared_y, 'int32')

    test_set_x, test_set_y = shared_dataset(test_set)
    valid_set_x, valid_set_y = shared_dataset(valid_set)
    train_set_x, train_set_y = shared_dataset(train_set)

    rval = [(train_set_x, train_set_y), (valid_set_x, valid_set_y),
            (test_set_x, test_set_y)]
    return rval

#CLASSIFIER, Last layer，LOGISTIC REGRESSION（softmax）
class LogisticRegression(object):
    def __init__(self, input, n_in, n_out):
        self.W = theano.shared(
            value=numpy.zeros(
                (n_in, n_out),
                dtype=theano.config.floatX
            ),
            name='W',
            borrow=True
        )
        self.b = theano.shared(
            value=numpy.zeros(
                (n_out,),
                dtype=theano.config.floatX
            ),
            name='b',
            borrow=True
        )
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


#FULL CONNECTION LAYER
class HiddenLayer(object):
    def __init__(self, rng, input, n_in, n_out, W=None, b=None,
                 activation=T.tanh):

        self.input = input

        if W is None:
            W_values = numpy.asarray(
                rng.uniform(
                    low=-numpy.sqrt(6. / (n_in + n_out)),
                    high=numpy.sqrt(6. / (n_in + n_out)),
                    size=(n_in, n_out)
                ),
                dtype=theano.config.floatX
            )
            if activation == theano.tensor.nnet.sigmoid:
                W_values *= 4
            W = theano.shared(value=W_values, name='W', borrow=True)

        if b is None:
            b_values = numpy.zeros((n_out,), dtype=theano.config.floatX)
            b = theano.shared(value=b_values, name='b', borrow=True)

        self.W = W
        self.b = b

        lin_output = T.dot(input, self.W) + self.b
        self.output = (
            lin_output if activation is None
            else activation(lin_output)
        )
        # parameters of the model
        self.params = [self.W, self.b]


#（conv+maxpooling）
class LeNetConvPoolLayer(object):

    def __init__(self, rng, input, filter_shape, image_shape, poolsize=(2, 2)):

        assert image_shape[1] == filter_shape[1]
        self.input = input

        fan_in = numpy.prod(filter_shape[1:])
        fan_out = (filter_shape[0] * numpy.prod(filter_shape[2:]) /
                   numpy.prod(poolsize))

        # initialize weights with random weights
        W_bound = numpy.sqrt(6. / (fan_in + fan_out))
        self.W = theano.shared(
            numpy.asarray(
                rng.uniform(low=-W_bound, high=W_bound, size=filter_shape),
                dtype=theano.config.floatX
            ),
            borrow=True
        )

        # the bias is a 1D tensor -- one bias per output feature map
        b_values = numpy.zeros((filter_shape[0],), dtype=theano.config.floatX)
        self.b = theano.shared(value=b_values, borrow=True)

        # CONVOLUTION
        conv_out = conv.conv2d(
            input=input,
            filters=self.W,
            filter_shape=filter_shape,
            image_shape=image_shape
        )

        # MAX POOLING
        pooled_out = downsample.max_pool_2d(
            input=conv_out,
            ds=poolsize,
            ignore_border=True
        )

        self.output = T.tanh(pooled_out + self.b.dimshuffle('x', 0, 'x', 'x'))

        # store parameters of this layer
        self.params = [self.W, self.b]


#save parameters
def save_params(param0_W, param0_b, param1_W, param1_b, param2_W, param2_b,
                param3_W, param3_b):
        import pickle
        write_file = open('params_BdV2.5.pkl', 'wb')
        pickle.dump([param0_W, param0_b, param1_W, param1_b, param2_W, param2_b,
                     param3_W, param3_b], write_file)
        write_file.close()



#put it together
class CNN(object):

    def __init__(self,layer0_input,rng,nkerns=[10, 15], batch_size=39):
     ######################
    #Building CNN model:
    #input+layer0(LeNetConvPoolLayer)+layer1(LeNetConvPoolLayer)+layer2(HiddenLayer)+layer3(LogisticRegression)
    ######################
        print '... building the model'

        # Reshape matrix of rasterized images of shape (batch_size, 37 * 50)
        # to a 4D tensor, compatible with our LeNetConvPoolLayer
        # (37, 50) is the size of images.

        # first layer , conv+pooling
        # after conv：(37-5+1,50-5+1) = (33, 46)
        # after maxpooling： (33/2,46/2) = (16, 23)，floor(x/2) ignoring edges
        # 4D output tensor is thus of shape (batch_size, nkerns[0], 16(height), 23(width))
        self.layer0 = LeNetConvPoolLayer(
            rng,
            input=layer0_input,
            image_shape=(batch_size, 1, 37, 50),
            filter_shape=(nkerns[0], 1, 5, 5),
            poolsize=(2, 2)
        )

        # second conv+pooling,input= output of first layer，el.(batch_size, nkerns[0], 16, 23)
        # after conv:(16-5+1 , 23-5+1) = (12, 19)
        # after maxpooling： (12/2, 19/2) = (6, 9)，floor() ignorting edges
        # 4D output tensor is thus of shape (batch_size, nkerns[1], 6,9)
        self.layer1 = LeNetConvPoolLayer(
            rng,
            input=self.layer0.output,
            image_shape=(batch_size, nkerns[0], 16, 23),
            filter_shape=(nkerns[1], nkerns[0], 5, 5),
            poolsize=(2, 2)
        )

        # HiddenLayer，input(nkern[1], num_pixels) = output of previous layer
        self.layer2_input = self.layer1.output.flatten(2)
        self.layer2 = HiddenLayer(
            rng,
            input= self.layer2_input,
            n_in=nkerns[1] * 9 * 6,
            n_out=2500,      #output neural connections, can be changed, normally greater is better.
            activation=T.tanh
        )

        #classifier
        #n_in hidden layer output，n_out = classification types
        self.layer3 = LogisticRegression(input=self.layer2.output, n_in=2500, n_out=5)

        # L1 norm ; one regularization option is to enforce L1 norm to
        # be small
        self.L1 = (
            abs(self.layer2.params[0].get_value()).sum()
            + abs(self.layer3.params[0].get_value()).sum()
        )

        # square of L2 norm ; one regularization option is to enforce
        # square of L2 norm to be small
        self.L2_sqr = (
            (self.layer2.params[0].get_value() ** 2).sum()
            + (self.layer3.params[0].get_value() ** 2).sum()
        )

        # negative log likelihood of the MLP is given by the negative
        # log likelihood of the output of the model, computed in the
        # logistic regression layer
        self.negative_log_likelihood = (
            self.layer3.negative_log_likelihood
        )
        # same holds for the function computing the number of errors
        self.errors = self.layer3.errors

        # the parameters of the model are the parameters of the two layer it is
        # made out of
        self.params = self.layer0.params+self.layer1.params + self.layer2.params+ self.layer3.params
        # end-snippet-3

def evaluate(learning_rate=0.01, n_epochs=300,
                    dataset='BdV2.5_reel_50_37_BW.save',
                     batch_size=39):

    #random generator, for initialisation of parameters W
    rng = numpy.random.RandomState(23455)
    #load data .save, load_data function is in logistic_sdg.py
    datasets = load_data(dataset)
    train_set_x, train_set_y = datasets[0]
    valid_set_x, valid_set_y = datasets[1]
    test_set_x, test_set_y = datasets[2]

    #calculate batchsize
    n_train_batches = train_set_x.get_value(borrow=True).shape[0]
    n_valid_batches = valid_set_x.get_value(borrow=True).shape[0]
    n_test_batches = test_set_x.get_value(borrow=True).shape[0]
    n_train_batches /= batch_size
    n_valid_batches /= batch_size
    n_test_batches /= batch_size

    #definition of x (images data), y: labels data
    index = T.lscalar()
    x = T.matrix('x')  
    y = T.ivector('y')

    layer0_input = x.reshape((batch_size, 1, 37, 50))
    classifier = CNN(layer0_input,rng)

    cost = (

        classifier.negative_log_likelihood(y)+0.0006*classifier.L2_sqr

    )

    # compiling a Theano function that computes the mistakes that are made
    # by the model on a minibatch
    test_model = theano.function(
        inputs=[index],
        outputs=classifier.errors(y),
        givens={
            x: test_set_x[index * batch_size:(index + 1) * batch_size],
            y: test_set_y[index * batch_size:(index + 1) * batch_size]
        }
    )

    validate_model = theano.function(
        inputs=[index],
        outputs=classifier.errors(y),
        givens={
            x: valid_set_x[index * batch_size:(index + 1) * batch_size],
            y: valid_set_y[index * batch_size:(index + 1) * batch_size]
        }
    )

    # start-snippet-5
    # compute the gradient of cost with respect to theta (sotred in params)
    # the resulting gradients will be stored in a list gparams
    gparams = [T.grad(cost, param) for param in classifier.params]

    # specify how to update the parameters of the model as a list of
    # (variable, update expression) pairs

    # given two list the zip A = [a1, a2, a3, a4] and B = [b1, b2, b3, b4] of
    # same length, zip generates a list C of same size, where each element
    # is a pair formed from the two lists :
    #    C = [(a1, b1), (a2, b2), (a3, b3), (a4, b4)]
    updates = [
        (param, param - learning_rate * gparam)
        for param, gparam in zip(classifier.params, gparams)
    ]

    # compiling a Theano function `train_model` that returns the cost, but
    # in the same time updates the parameter of the model based on the rules
    # defined in `updates`
    train_model = theano.function(
        inputs=[index],
        outputs=cost,
        updates=updates,
        givens={
            x: train_set_x[index * batch_size: (index + 1) * batch_size],
            y: train_set_y[index * batch_size: (index + 1) * batch_size]
        }
    )
    # end-snippet-5

    ###############
    # TRAIN MODEL #
    ###############
    print '... training'

    # early-stopping parameters
    patience = 72800  # look as this many examples regardless
    patience_increase = 2  # wait this much longer when a new best is
                           # found
    improvement_threshold = 0.995  # a relative improvement of this much is
                                   # considered significant
    validation_frequency = min(n_train_batches, patience / 2)
                                  # go through this many
                                  # minibatche before checking the network
                                  # on the validation set; in this case we
                                  # check every epoch

    best_validation_loss = numpy.inf
    best_iter = 0
    test_score = 0.
    start_time = time.clock()

    epoch = 0
    done_looping = False
    while (epoch < n_epochs) and (not done_looping) :
        epoch = epoch + 1
        for minibatch_index in xrange(n_train_batches):

            minibatch_avg_cost = train_model(minibatch_index)

            # iteration number
            iter = (epoch - 1) * n_train_batches + minibatch_index

            if (iter + 1) % 45 == 0:
                # compute zero-one loss on validation set
                validation_losses = [validate_model(i) for i
                                     in xrange(n_valid_batches)]
                this_validation_loss = numpy.mean(validation_losses)
                print(
                    'epoch %i, minibatch %i/%i, validation error %f %%' %
                    (
                        epoch,
                        minibatch_index + 1,
                        n_train_batches,
                        this_validation_loss * 100.
                    )
                )
                print('cost %f: '%(minibatch_avg_cost))
                # if we got the best validation score until now
                if this_validation_loss < best_validation_loss:
                    #improve patience if loss improvement is good enough
                    if (
                        this_validation_loss < best_validation_loss *
                        improvement_threshold
                    ):
                        patience = max(patience, iter * patience_increase)

                    best_validation_loss = this_validation_loss
                    best_iter = iter

                    # test it on the test set
                    test_losses = [test_model(i) for i
                                   in xrange(n_test_batches)]
                    test_score = numpy.mean(test_losses)

                    print(('     epoch %i, minibatch %i/%i, test error of '
                           'best model %f %%') %
                          (epoch, minibatch_index + 1, n_train_batches,
                           test_score * 100.))
                    print ("get lower error rate, save parameters...")
                    #save params if getting lower error rate
                    save_params(classifier.layer0.params[0],classifier.layer0.params[1],classifier.layer1.params[0],
                                classifier.layer1.params[1],classifier.layer2.params[0],classifier.layer2.params[1],
                                classifier.layer3.params [0],classifier.layer3.params [1])#save params

            if patience <= iter:
                done_looping = True
                break
    end_time = time.clock()
    print(('Optimization complete. Best validation score of %f %% '
           'obtained at iteration %i, with test performance %f %%') %
          (best_validation_loss * 100., best_iter + 1, test_score * 100.))
    print >> sys.stderr, ('The code for file ' +
                          os.path.split(__file__)[1] +
                          ' ran for %.2fm' % ((end_time - start_time) / 60.))



if __name__ == '__main__':
	evaluate()
