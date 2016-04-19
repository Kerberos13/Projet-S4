mnist.pkl.gz : Les données pour l'entrainement 

model.pkl.gz : résultat(objets des couches) de l'entrainement pour LeNet-5 handwriting

single_image.pkl.gz : donnees binaire sur une image pour la prediction

deep_learning_test1.py : fichier python pour l'entrainement, le test des résultat, la validation des résultat

logistic_sgd.py : il est servi pour la dernière couches du LeNet-5. "logistic regression using statistic gradient descente"

dataset_GENER: pour enregister l'image en "pkl.gz"

mlp.py : il est servi pour la couche cachée(hidden layer) du LeNet-5.

prediction.py : predire la classe auquelle apartient l'image enregistree sous forme de "pkl.gz".

main : qui fait tout sauf entrainement

les explications plus préciseq sur les fichiers dessus sont disponibles sur des liens suivants:
leNet :
http://deeplearning.net/tutorial/lenet.html

logistic Regression (logistic_sgd.py ) :
http://deeplearning.net/tutorial/logreg.html

Multilayer Perceptron (mlp.py) :
http://deeplearning.net/tutorial/mlp.html

Les fichiers python ont besoin de bibiotheque Theano, guide de l'installation :
http://deeplearning.net/software/theano/install.html

Faire attention à la dépendance des "packages" de Theano : Scipy, Numpy
Solution plus simple : utilisez IDE comme "JetBrains Pycharm Community"

la Python 2 fonctionne mieux, mais Python 3 marche aussi.

