function VisualisationClothilde

% Les param�tres suivants ne sont normalement pas � modifier :
Fe = 3456e3 ; % Fr�quence d'�chantillonage du capteur CLOTHILDE= 3456 kHz 
ResolF = 100 ; % R�solution en Hz de la canalisation d'analyse
% Les param�tres � modifier sont :
% Nom /chemin du fichier en entr�e (lenregistrement CLOTHILDE � traiter) :
NonFic = 'J:\Deep learning\SignauxHF_Clothilde\HF_3700.iq' ;
fic = fopen(NonFic,'rb') ;
W = fread(fic,'int16');
DimSig = fix(length(W)/2) ;

% Calcul des canaux et du temps/fr�quence :
z = double(W(1:2:2*DimSig-1)) +1i* double(W(2:2:2*DimSig));
clear W
Nfft = round(Fe/ResolF) ;
[Spectre,TF,Canaux,Axe_Temps,Axe_Freq] = DSP(z,Nfft,3,100,0.5,1); %(x,Nfft,R,Niv_Rejection,Recouvrement,NbMoy)
clear Canaux
TF = 10*log10(TF) ;
Spectre = 10*log10(Spectre) ;

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


% Visualisation de l'image temps/fr�quence et du spectre :
figure(1);
imagesc(TF');
figure(2);
plot(Spectre);
a=1;


