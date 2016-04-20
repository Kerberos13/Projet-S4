function TraiterRepertoir(RepertoirSignaux)
% Scripe permettant de traiter tous les fichiers d'un r�pertoir

% Si pas de r�pertoir en entr�e, on demande � l'op�rateur d'en saisir un :
if nargin <1  
    RepertoirSignaux = uigetdir ;
    if isequal(RepertoirSignaux,0)
       return ; % Aucune saisie
    end
end

qstring = ['voulez-vous traiter tous les signaux du r�pertoir : ',RepertoirSignaux] ;
button = questdlg(qstring,'Confirmation','Non','Oui','Oui');
if strcmp(button, 'Oui')
    TabFic = dir(RepertoirSignaux);
    TraitSousRepertoir = 0;
    for n = 1:length(TabFic)
        if strcmp(TabFic(n).name,'.') continue; end
        if strcmp(TabFic(n).name,'..') continue; end
        if TabFic(n).isdir
            button2 = questdlg('Voulez-traiter �galement les sous-r�pertoirs ?','Sous Repertoir ?','Non','Oui','Oui');
            if strcmp(button2, 'Oui')
                TraitSousRepertoir = 1;
            end
            break;
        end
    end
    NbSignaux = CompterFichierType(RepertoirSignaux, '.wav', TraitSousRepertoir);
    if NbSignaux >= 1
        qstring = sprintf('Il y a %d signaux � traiter. Confirmez-vous le lancement des traitements ?',NbSignaux);
        button = questdlg(qstring,'Confirmation','Non','Oui','Oui');
        if strcmp(button,'Oui')
            % On cr�e la barre d'attente :
            h_waitbarr = waitbar(0,'Initialisation','Name','Suivi des traitements',...
                'CreateCancelBtn',...
                'setappdata(gcbf,''canceling'',1)');
            setappdata(h_waitbarr,'canceling',0);
            NbSignauxTraites = CalculerSignaux(RepertoirSignaux, '.wav', TraitSousRepertoir, h_waitbarr, NbSignaux);
            delete(h_waitbarr) ;
            Message = sprintf('%d signaux ont �t� trait�s sur %d',NbSignauxTraites,NbSignauxATraiter) ;
            h = msgbox(Message) ;
            uiwait(h);
        end
    else
        h = warndlg('Aucun signal � traiter n''a �t� trouv� dans le r�pertoir !','modal');
        uiwait(h);
    end
end