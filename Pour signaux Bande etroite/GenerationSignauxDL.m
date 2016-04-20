%Fonction dirr, lire tous les fichier dans le repertoire. Output: les addr
%des fichier
fl=dirr('F:\bd_s4\Deep learning\TEST');
nl=length(fl);
for i=1:nl
        fname=fl(i).name;
        str=['F:\bd_s4\Deep learning\TEST\',fl(i).name];
        GenerationSignauxDL_v2(str);
        
end