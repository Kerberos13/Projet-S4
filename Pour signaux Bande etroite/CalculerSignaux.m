function NbSignauxTraites = CalculerSignaux(Rep, Type, TraitSousRepertoir, h_waitbarr, NbSignauxATraiter)
% fonction qui lance le traitement de tous les fichier trouvés dont 
% l'extension est Type et qui sont présents dans le répertoir Rep.
% Si TraitSousRepertoir = 1, il traite également les fichiers présents dans
% les sous-répertoirs.
% Le nombre total de fichiers traités est renvoyé dans NbSignauxTraites

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
                sprintf('Traitement du %d ème signal sur %d',NbSignauxTraites+1,NbSignauxATraiter));
            NomFichier = [Rep,'\', Tab(n).name] ;
            GenerationSignauxDL(NomFichier) ;
            NbSignauxTraites = NbSignauxTraites+1;
        end
    end
end

