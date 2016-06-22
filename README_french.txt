                                      #-#-#    R E A D   M E   #-#-#


Ce logiciel a pour but de reconnaître la modulation d'un signal donné en utilisant un Réseau de Neurones Artificiel. Il a été 
développé dans le cadre d'un projet à Télécom Bretagne, et est basé sur une idée proposée par INEO Défense.


Pour lancer le logiciel, deux options sont actuellement disponibles. Vous pouvez soit le lancer directement en mode console en
tapant "python main.py <chemin_du_fichier>" dans un terminal, où <chemin_du_fichier> peut être un chemin relatif ou absolu vers
le spectrogram ou le signal, ou en utilisant l'interface graphique en tapant "python ProjetS4.py".


Les chemins relatifs et absolus sont tous les deux acceptés. Les images scindées et le spectrogramme analysé sont tous disponibles
dans le dossier "tmp/", en fonction de l'avancement du calcul.
Pour le moment, seul les fichiers de type .jpg, .bmp ou .wav sont supportés. Dans le cas d'un fichier .wav, un spectrogram sera
généré automatiquement et enregistré en tant que .jpg.


Pythons est très sensible à l'indentation. Les fichiers actuels sont écrits avec une indentation de quatre espaces. Nous vous
invitons à respecter cette indentation si vous êtes amenés à modifier une partie des fichiers existants, où le programme ne pourra
être compilé.


Ce programme a plusieurs dépendances et a besoin que différents éléments soient installés afin de fonctionner : Python3 (un mode
compatibilité est cependant disponible pour python 2), numpy, scipy, pillow et theano. Si vous essayez de le lancer sans installer
les dépendances, un message d'erreur devrait apparaître et vous inviter à lancer le script setup.py. Veuillez noter que ce script
a besoin d'être lancé avec les privilèges d'administrateur.
De manière générale, nous vous invitons à lancer ce logiciel depuis un terminal, et non en cliquant directement dessus, car 
davantage de messages apparaîtront ainsi, ce qui peut être utile en cas de comportement inattendu.


L'interface graphique utilise tkinter, qui est incluse par défaut avec Python. Vous pouvez sélectionner un fichier à l'aide du
bouton dédié, régler les paramètres de seuil, de marge, l'épaisseur et la couleur des lignes, et choisir entre le réseau de neurones
de type CNN ou SDA à l'aide de l'interrupteur approprié. Le bouton compute lancera alors le calcul et affichera le spectrogram.
Nous tenons à souligner que par défaut, la valeur des marges devrait être réglée sur 10, puisque la base de données à été générée
avec cette valeur. La possibilité d'utiliser des marges plus faibles reste toutefois disponible car elle peut s'avérer utile lors
de l'utilisation de matériel SDR.


Le logiciel possède plusieurs modules. Pour simplifier, le module principal commence par appeler le module spectrogram si nécessaire
afin de générer le spectrogram, puis il appelle le module sign_detect2 afin de détecter les signaux présents. Ensuite, il appelle
le module resize qui va générer les matrices utilisables directement par le RNA. Le module use_CNN_compatible est alors appelé
afin d'obtenir la prédiction du RNA. Enfin, le spectrogramme est réassemblé à l'aide du module reass. Si l'interface graphique
est utilisée, le module ProjetS4 affichera l'interface graphique et procédera de manière similaire au module principal. Presque
tous les modules ont des fonctions en commun qui sont rassemblées dans le module tools.



Contact: s4-projet-52-2016@mlistes.telecom-bretagne.eu
         benoit.porteboeuf@telecom-bretagne.eu
