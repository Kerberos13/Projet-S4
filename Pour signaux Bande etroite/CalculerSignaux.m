function NbSignauxTraites = CalculerSignaux(Rep, Type, TraitSousRepertoir, h_waitbarr, NbSignauxATraiter)
% fonction qui lance le traitement de tous les fichier trouv�s dont 
% l'extension est Type et qui sont pr�sents dans le r�pertoir Rep.
% Si TraitSousRepertoir = 1, il traite �galement les fichiers pr�sents dans
% les sous-r�pertoirs.
% Le nombre total de fichiers trait�s est renvoy� dans NbSignauxTraites

NbSignauxTraites = 0;
Tab = dir(Rep);
for n = 1:length(Tab)
    if strcmp(Tab(n).name,'.') continue; end
    if strcmp(Tab(n).name,'..') continue; end
    if Tab(n).isdir
        if TraitSousRepertoir==1
            SousRep = [Rep,'\',Tab(n).name];
            N = CalculerSignaux(SousRep, Type, TraitSousRepertoir, h_waitbarr, NbSignauxATraiter);
            NbSignauxTraites = NbSignauxTraites + N;
        end
    else
    	[start_path, name, ext] = fileparts(Tab(n).name);
        if strcmp(ext, Type)
            if getappdata(h_waitbarr,'canceling')
                return;
            end
            % Report current estimate in the waitbar's message field
            waitbar(NbSignauxTraites+1/NbSignauxATraiter, ...
                h_waitbarr, ...
                sprintf('Traitement du %d �me signal sur %d',NbSignauxTraites+1,NbSignauxATraiter));
            NomFichier = [Rep,'\', Tab(n).name] ;
            GenerationSignauxDL(NomFichier) ;
            NbSignauxTraites = NbSignauxTraites+1;
        end
    end
end

