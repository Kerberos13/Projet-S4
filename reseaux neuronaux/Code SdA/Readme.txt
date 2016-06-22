Il y a deux parties dans SdA, l'une pour entrainer le réseau neuronal et l'autre pour prédire le résultat.

Le fichier SdA est pour entrainer le réseau neuronal, dans ce fichier, la fonction test_SdA est l'entrée, les attributs 'fine_lr' et 'pretrain_lr' signigient respectivement taux d'apprentissage pour prétrainement et traitement, 'pretraining_epochs' et 'training_epochs'signifient respectivement nb d'itération pour prétraitement et traitement.En fin, 'dataset' signifie les données qu'on va utiliser.

Pour prédire les données,il suffit de lancer la foncton test_SdAForPicture, 'dataset' signifie le dossier d'image qu'on va prédire et 'params_file' est le fichier comportant les paramètres obtenu pendant l'entrainement.