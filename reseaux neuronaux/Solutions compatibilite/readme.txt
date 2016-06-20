pour le probème de CPU_GPU compatibilité :

à la sortie de l'entraînement, on sauvegarde les paramètres en CUDAarray, ce type ne peut pa s'utilise par un CPU.

Pour résoudre le problème de compabilité, on utilise un code sur 
https://github.com/lisa-lab/pylearn2
Soruce :
Ian J. Goodfellow, David Warde-Farley, Pascal Lamblin, Vincent Dumoulin, 
Mehdi Mirza, Razvan Pascanu, James Bergstra, Frédéric Bastien, and Yoshua Bengio.
 "Pylearn2: a machine learning research library". arXiv preprint arXiv:1308.4214 (BibTeX)


Dans le dossier "scripts", utilisez le fichier gpu_pkl_to_cpu_pkl.py pour transformer les paramètres enregistrés
sous forme ".pkl"  en un nouveau ".pkl" utilisable pour CPU.




pour le probème de CPU_GPU compatibilité :

pickel n'est pas compatible entre Python2 et Python3.

s'il y a  des sourcis, merci d'essayer de changer tous les codes "pickel.load(xxx)" en "pickel.load(xxx,encoding = "bytes")"