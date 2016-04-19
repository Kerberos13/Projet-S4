__author__ = 'yxu01'
import cPickle
import gzip
from deep_learning_test1 import LeNetConvPoolLayer
import theano
import numpy as np
def shared_dataset(data_xy, borrow=True):
    """ Function that loads the dataset into shared variables

    The reason we store our dataset in shared variables is to allow
    Theano to copy it into the GPU memory (when code is run on GPU).
    Since copying data into the GPU is slow, copying a minibatch everytime
    is needed (the default behaviour if the data is not in a shared
    variable) would lead to a large decrease in performance.
    """
    data_x = data_xy
    shared_x = theano.shared(np.asarray(data_x,dtype=theano.config.floatX),borrow=borrow)
    # When storing data on the GPU it has to be stored as floats
    # therefore we will store the labels as ``floatX`` as well
    # (``shared_y`` does exactly that). But during our computations
    # we need them as ints (we use labels as index, and if they are
    # floats it doesn't make sense) therefore instead of returning
    # ``shared_y`` we will have to cast it to int. This little hack
    # lets ous get around this issue
    return shared_x

def predict(testset,batch_size,model='./model.pkl.gz'):

      """ Load a trained model and use it to predict labels.

      :type model: Layers to accept inputs and produce outputs.
      """

      # Load the saved model.
      classifiers = cPickle.load(gzip.open(model))

      # Pick out the individual layer
      layer0_input = classifiers[0]
      layer3 = classifiers[5]

      # Apply it to our test set
      f = gzip.open(testset, 'rb')
      test_set = cPickle.load(f)
      f.close()
      test_set_x = shared_dataset(test_set)
      inputs = np.asanyarray(test_set_x.get_value(borrow=True),dtype=theano.config.floatX)

      # compile a predictor function

      predict_model = theano.function(
          [layer0_input],
          layer3.y_pred,
      )

      predicted_values = predict_model(
          inputs[:batch_size].reshape((batch_size, 1, 28, 28))
      )


      print('Prediction complete.')
      return predicted_values


