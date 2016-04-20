function TraiterRepertoir(RepertoirSignaux)
% Scripe permettant de traiter tous les fichiers d'un répertoir

% Si pas de répertoir en entrée, on demande à l'opérateur d'en saisir un :
if nargin <1  
    RepertoirSignaux = uigetdir ;
    if isequal(RepertoirSignaux,0)
       return ; % Aucune saisie
    end
end

qstring = ['voulez-vous traiter tous les signaux du répertoir : ',RepertoirSignaux] ;
button = questdlg(qstring,'Confirmation','Non','Oui','Oui');
if strcmp(button, 'Oui')
    TabFic = dir(RepertoirSignaux);
    TraitSousRepertoir = 0;
    for n = 1:length(TabFic)
        if strcmp(TabFic(n).name,'.') continue; end
        if strcmp(TabFic(n).name,'..') continue; end
        if TabFic(n).isdir
            button2 = questdlg('Voulez-traiter également les sous-répertoirs ?','Sous Repertoir ?','Non','Oui','Oui');
            if strcmp(button2, 'Oui')
                TraitSousRepertoir = 1;
            end
            break;
        end
    end
    NbSignaux = CompterFichierType(RepertoirSignaux, '.wav', TraitSousRepertoir);
    if NbSignaux >= 1
        qstring = sprintf('Il y a %d signaux à traiter. Confirmez-vous le lancement des traitements ?',NbSignaux);
        button = questdlg(qstring,'Confirmation','Non','Oui','Oui');
        if strcmp(button,'Oui')
            % On crée la barre d'attente :
            h_waitbarr = waitbar(0,'Initialisation','Name','Suivi des traitements',...
                'CreateCancelBtn',...
                'setappdata(gcbf,''canceling'',1)');
            setappdata(h_waitbarr,'canceling',0);
            NbSignauxTraites = CalculerSignaux(RepertoirSignaux, '.wav', TraitSousRepertoir, h_waitbarr, NbSignaux);
            delete(h_waitbarr) ;
            Message = sprintf('%d signaux ont été traités sur %d',NbSignauxTraites,NbSignauxATraiter) ;
            h = msgbox(Message) ;
            uiwait(h);
        end
    else
        h = warndlg('Aucun signal à traiter n''a été trouvé dans le répertoir !','modal');
        uiwait(h);
    end
end