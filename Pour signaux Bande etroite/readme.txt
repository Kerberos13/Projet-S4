Ces fichiers sont utilis¨¦ pour traiter les donn¨¦es .wav fournies par notre client.

PS: il existe des don¨¦es .iq (large bande), les scripts pour traiter cela seront fourni dans cette semaine...


mode d'emploi :
lancer le script "GenerationSignauxDL.m"

ce script, il utilise "dirr.m" pour la lecture des fichiers .wav ¨¦tant don¨¦¨¦ l'adresse. En suite, il
calcule le transform¨¦ de fourier du signal avec "PreCalcul2.m". A la fin, dans le script "PreCalcul2.m",
il lance le script "PlotVisuSignal_2.m".

les images en sortie sont sans axes.

Si vous avez besoin des axes dans l'image (des info fr¨¦quences, temps).
Allez vers le script "PlotVisuSignal_2.m", la version avec axes est en commentaire.

Concernant l'enregistrement des images :
les images sont enregistre¨¦s dans le m¨ºme que les fichier en entr¨¦e.
le nom de l'image est pareil comme le fichier (qui peut ¨ºtre utilis¨¦ comme label).

Attention : 
le fichier dirr ne peut que lire les fichiers dans un r¨¦pertoire, c-¨¤-d, il est interdit de mettre

un autre r¨¦pertoire dans un r¨¦pertoire. le r¨¦pertoire ¨¤ lire doit contenir que des fichiers .wav. 


