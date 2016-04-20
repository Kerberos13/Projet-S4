function NbFichiers = CompterFichierType(Rep, Type, TraitSousRepertoir)
% fonction qui calcule le nombre de fichier dont l'extension est Type et qui
% sont pr�sents dans un r�pertoir.
% Si TraitSousRepertoir = 1, il compte �galement les fichiers pr�sents dans
% les sous-r�pertoirs.
% Le nombre total de fichiers comptabilis�s est renvoy� dans NbFichiers

NbFichiers = 0;
Tab = dir(Rep);
for n = 1:length(Tab)
    if strcmp(Tab(n).name,'.') continue; end
    if strcmp(Tab(n).name,'..') continue; end
    if Tab(n).isdir
        if TraitSousRepertoir==1
            SousRep = [Rep,'\',Tab(n).name];
            N = CompterFichierType(SousRep, Type, TraitSousRepertoir);
            NbFichiers = NbFichiers + N;
        end
    else
    	[start_path, name, ext] = fileparts(Tab(n).name);
        if strcmp(ext, Type)
            NbFichiers = NbFichiers+1;
        end
    end
end

