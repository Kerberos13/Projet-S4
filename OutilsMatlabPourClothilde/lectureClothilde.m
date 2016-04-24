function lectureClothilde
clear all
% Fonction de lecture des fichiers d'enregistrement produits par le
% capteur CLOTHILDE et de conversion en :
% - un fichier I/Q brut : extension .iq
% - un fichier image temps/fr�quence : extension .tf
% - un fichier signal canalis� : extension .cnx
% Le script permet aussi de visulasiser le spectre et le temps/fr�quence
%
% Les param�tres suivants ne sont normalement pas � modifier :
Fe = 3456e3 ; % Fr�quence d'�chantillonage du capteur CLOTHILDE= 3456 kHz 
ResolF = 100 ; % R�solution en Hz de la canalisation d'analyse
% Les param�tres � modifier sont :
% Nom /chemin du fichier en entr�e (lenregistrement CLOTHILDE � traiter) :
NonFicEngrt = 'F:\bd_s4\Deep learning\SignauxHF_Clothilde\HF_9750kHz.data' ;
% Nom / chemin des fichiers produits en sortie :
NonFicSortie = 'F:\bd_s4\Deep learning\SignauxHF_Clothilde\HF_9750kHz' ;
% longueur du fichier I/Q brut souhait�, en nombre d'I/Q
DimSig = 3*13500*256 ; % 3 secondes de signal

% Lecture du fichier d'enregistrement CLOTHILDE :
fic = fopen(NonFicEngrt,'rb') ;
W = zeros(2*DimSig,1,'int16');
t = 0 ;
t_fin = DimSig / 256; % Nombre de fois qu'on doit lire un bloc de 256 �chantillons
while t < t_fin 
    canal = fread(fic,1,'uint8') ;
    if isempty(canal) % Fin pr�matur�e du fichier
        DimSig = t*256 ;
        break ;
    end
    fseek(fic,19,'cof');
%     % lecture suite de l'ent�te :
%     compteur = fread(fic,1,'uint8') ;
%     timestamp = fread(fic,1,'uint64') ;
%     flagsFPGA = fread(fic,1,'uint8') ;
%     flagsUser = fread(fic,1,'uint8') ;
%     decim = fread(fic,1,'uint8') ;
%     gain = fread(fic,1,'uint8') ;
%     flags = fread(fic,1,'uint16') ;
%     frf = fread(fic,1,'uint32') ;
    if canal == 0
        W(2*t*256+1 : 2*(t+1)*256) = fread(fic,2*256,'int16') ;
%         for k = t*256+1:t*256+256
%             W(2*k-1) = fread(fic,1,'int16') ;
%             W(2*k) = fread(fic,1,'int16') ;
%         end
        t = t+1 ;
    else
        fseek(fic,1024,'cof');
    end
end
fclose(fic);

% Enregistrement du fichier I/Q brut :
fiq = fopen([NonFicSortie,'.iq'],'wb') ;
fwrite(fiq,W(1:2*DimSig),'int16') ;
fclose(fiq);

% Calcul des canaux et du temps/fr�quence :
z = double(W(1:2:2*DimSig-1)) +1i* double(W(2:2:2*DimSig));
clear W
Nfft = round(Fe/ResolF) ;
[Spectre,TF,Canaux,Axe_Temps,Axe_Freq] = DSP(z,Nfft,3,100,0.5,1); %(x,Nfft,R,Niv_Rejection,Recouvrement,NbMoy)
fcnx = fopen([NonFicSortie,'.cnx'],'wb') ;
fwrite(fcnx,Canaux,'float') ;
fclose(fcnx);
clear Canaux
ftf = fopen([NonFicSortie,'.tf'],'wb') ;
TF = 10*log10(TF) ;
fwrite(ftf,TF,'float') ;
fclose(ftf);
fspt = fopen([NonFicSortie,'.spt'],'wb') ;
Spectre = 10*log10(Spectre) ;
fwrite(fspt,Spectre,'float') ;
fclose(fspt);

% correction du niveau z�ro avec pour objectif rendre plat le planch� de
% bruit
N = 1000; D = 500;
nbP = 1 + floor((Nfft-N) / D);
Brc = zeros(nbP,1) ;
edges = floor(min(Spectre)) : ceil(max(Spectre)) ;
for k = 1 : nbP
    H = histc(Spectre(1+(k-1)*D : (k-1)*D+N),edges) ;
    [bid,Brc(k)] = max(H) ;
end
Brd = [edges(Brc(1)), edges(Brc), edges(Brc(end))];
Brf = filtfilt(ones(5,1)/5,1,Brd);
% figure(1); % Pour d�bug
% plot(1:nbP+2, Brd,1:nbP+2,Brf);
Y = ( 0 : D : (nbP-1)*D) + round(N/2) ;
Y = [1 , Y , Nfft];
Bruit = interp1(Y , Brf , 1:Nfft , 'spline','extrap') ;
% figure(2); % Pour d�bug
% plot(1:Nfft , Spectre , 1:Nfft , Bruit);
for k = 1:length(Axe_Temps) % Boucle pour r�duire l'espace m�moire n�cessaire
    TF(:,k) = TF(:,k) - Bruit' ;
end
Spectre = Spectre - Bruit' ;

ftfc = fopen([NonFicSortie,'.tfc'],'wb') ;
fwrite(ftfc,TF,'float') ;
fclose(ftfc);
fspc = fopen([NonFicSortie,'.spc'],'wb') ;
fwrite(fspc,Spectre,'float') ;
fclose(fspc);

% Visualisation de l'image temps/fr�quence et du spectre :
%without axis
fig1 = figure(1);
imagesc(TF');
set(gca,'position',[0 0 1 1],'units','normalized')
axis off
[pathstr, name, ext] = fileparts(NonFicEngrt) ;
%saveas(gca,[pathstr,'\',name, '.jpg'])
print (fig1 ,name,'-djpeg','-r600');


%with axis
fig2 =figure(2);
imagesc(TF');
print (fig2 ,[name,'_reference_freq'],'-djpeg','-r600');




