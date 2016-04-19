__author__ = 'yxu01'
import cPickle
import gzip
from logistic_sgd import LogisticRegression, load_data
from mlp import HiddenLayer
from deep_learning_test1 import LeNetConvPoolLayer
import theano
import theano.tensor as T
import numpy as np

def predict(model='./model.pkl.gz',
            testset='./mnist.pkl.gz',
            batch_size=5):

        """ Load a trained model and use it to predict labels.

        :type model: Layers to accept inputs and produce outputs.
        """

        # Load the saved model.
        classifiers = cPickle.load(gzip.open(model))

        # Pick out the individual layer
        layer0_input = classifiers[0]
        layer0 = classifiers[1]
        layer1 = classifiers[2]
        layer2_input = classifiers[3]
        layer2 = classifiers[4]
        layer3 = classifiers[5]

        # Apply it to our test set
        datasets = load_data(testset)
        test_set_x, test_set_y = datasets[2]
        #test_set_x = datasets[0]
        inputs = np.asanyarray(test_set_x.get_value(borrow=True),dtype=theano.config.floatX)
        print inputs.shape
        print inputs[1]
        # compile a predictor function
        index = T.lscalar()

        predict_model = theano.function(
          [layer0_input],
          layer3.y_pred,
        )

        predicted_values = predict_model(
          inputs[batch_size:batch_size*2].reshape((batch_size, 1, 28, 28))
        )


        print('Prediction complete.')
        #yy = test_set_y[batch_size:batch_size*2].eval()
        #print(yy)
        #rate = T.mean(T.neq(predicted_values, yy))
        #print(rate.eval())
        return predicted_values



#old version :result = predict('./model.pkl.gz','./mnist.pkl.gz',500)
result = predict('./model.pkl.gz','./mnist.pkl.gz',500)
print(result)