function [Spectre,TF,Cannaux,Axe_Temps,Axe_Freq] = DSP(x,Nfft,R,Niv_Rejection,Recouvrement,NbMoy,NumFig,DecFreq,Fentr)
%DSP spectre,temps/fr�quence et canalisation
% Calcule la DSP du signal x ;
% Plus pr�cis�ment, calcule le spectre de DSP, le diagramme temps/fr�quence
% de la DSP et une canalisation du signal. Quelques informations
% supl�mentaires sont �galement calcul�es.
%
% EXEMPLES D'UTILISATION :
% Sptr = DSP(Sig) (retourne dans Sptr le Spectre de Sig)
% [S,Dia] = DSP(Sig) (retourne le spectre et le diagramme temps fr�quence)
% Sptr = DSP(Sig,4096) (Calcule le spectre avec des FFT de 4096 points)
% [S,Dia] = DSP(Sig,[],[],[],[],5) (calcul le diagramme temps
% fr�quence avec un moyennage de 5 FFT pour chaque indice temporel)
% Seules les sorties demand�es sont calcul�es et la plupart des entr�es
% sont optionnelles.
% 
% EN ENTREE :
% x est soit un vecteur, soit un tableau. 
% Les autres param�tres sont optionnelles.
% Nfft = nombre de points du spectre (Par defaut 1024 si pas sp�cifi�)
% R = nombre de longeur FFT additionn�es dans le WOLA. R est entier >= � 1. 
% Si R=1, alors il n'y a qu'une seule longeur FFT utilis�e et l'algorithme
% se r�duit donc simplement � une fen�tre glissante. Si R >=2, on est donc
% avec un v�ritable WOLA. (par d�faut R=1)
% Niv_Rejection = niveau de r�jection en dB (110 dB par d�faut)
% Recouvrement : Chaque fen�tre de fft est d�cal�e de NxRecouvrement
% par rapport � la fen�tre pr�c�dente (par d�faut Recouvrement = 0.3)
% NbMoy = nombre de spectre moy�nn� pour calculer une ligne du diagramme
% temps fr�quence. (par d�faut, NbMoy=1) NbMoy est entier >= � 1.
% NumFig : num�ro de la figure o� sera affich� le spectre, si affichage
% DecFreq = d�calage en fr�quence appliqu� sur le signal. Ce param�tre
% permet de remettre les bin de FFT bien call� en fr�quence sur  le centre
% des �missions attendues (par d�faut = 0). Sp�cifi� en fr�quence r�duite : 
% si dF est le vrai d�calage � appliquer en Hertz et si Fe est la fr�quence
% d'�chantillonnage, alors DecFreq = dF/Fe
% Fentr : permet de sp�cifier la fen�tre a utiliser. Par d�faut, la
% fonction utilise une fen�tre de Kaiser. Si on veut utiliser une autre
% fen�tre, il faut la communiquer � la fonction dans Fentr. La longueur de
% Fentr doit �tre �gale � RxNfft. Si Fentr est utilis�, alors le param�tre 
% Niv_Rejection est sans effet.
%
% Utilise une fen�tre de kaiser de longueur RxNfft et param�tr�e pour avoir
% le niveau de r�jection correspondant � Niv_Rejection
% La fen�tre est normalis�e pour avoir un spectre de niveau  0 dB pour un
% signal CW de type exp(2*i*pi*freq*t) (c'est � dire une exponentiel
% complexe d'amplitude 1 )
% 
% EN SORTIE :
% Si il n'y a pas de sortie, DSP(x) affiche le spectre de x, dans la figure
% de num�ro NumFig ou dans la fen�tre 1 si Numfig n'est pas sp�cifi�
% si non,
% Spectre = le spectre de puissance (DSP) du signal x. Si x est un tableau,
% alors Spectre est un tableau dont chaque colone est la DSP d'un signaux
% de x
% TF = diagramme temps/fr�quence de l'�nergie du signal x. Si x est un
% tableau, alors on cumul toutes les puissances des signaux de x pour 
% construitre le diagramme TF
% Cannaux = signal canalis�
% Axe_Temps = vecteur contenant l'instant, en nombre d'�chantillons, des  
% indices temporels du diagramme TF. Si Fe est la fr�quence d'�chantillonnage en
% Hertz, alors Axe_Temps/Fe est l'axe temporel en seconde.
% Axe_Freq = vecteur contenant les fr�quences des bins. Les fr�quences sont
% indiqu�es en fr�quence r�duite : si Fe est la fr�quence
% d'�chantillonnage, alors Axe_Freq*Fe sont les fr�quences en Hertz.

if (nargin < 9)|| isempty(Fentr) % Si la fen�tre n'est pas sp�cifi�e, 
    Fentr = 0; % 
end
if (nargin <8)||isempty(DecFreq) % Si pas de d�calage en fr�quence de sp�cifi�, 
    DecFreq = 0; % le d�calage est nul
end
if (nargin <7)||isempty(NumFig) % Si la figure n'est pas sp�cifi� par les param�tres d'entr�es, 
    NumFig = 1; % on utilise la figure n� 1.
end
if (nargin <6)||isempty(NbMoy) % Si la moyenne n'est pas sp�cifi� par les param�tres d'entr�es, 
    NbMoy = 1; %  par d�faut pas de moyennage.
end
if (nargin <5)||isempty(Recouvrement) % Si le recouvrement n'est pas sp�cifi� par les param�tres d'entr�es, 
    Recouvrement = 0.3; % recouvrement par d�faut.
                        % Chaque fen�tre de fft est d�cal�e de 0.3xN de la fen�tre pr�c�dente
end
if (nargin <4)||isempty(Niv_Rejection) % Si la r�jection n'est pas sp�cifi�e par les param�tres d'entr�es, 
    Niv_Rejection = 110; % 110 dB de r�jection par defaut
end
if (nargin <3)||isempty(R) % Si la r�jection n'est pas sp�cifi�e par les param�tres d'entr�es, 
    R = 1; % donc par defaut pas de WOLA  mais simplement une FFT glissante
end
if (nargin <2)||isempty(Nfft) % Si le nombre de points de la fft n'est pas sp�cifi� par les param�tres d'entr�es, 
    if Fentr ~= 0 % La fen�tre est sp�cifi�e, mais pas Nfft
        Nfft = length(Fentr) / R ;
        if ~isinteger(Nfft)
            error('Dimensions de la fen�tre incompatible avec le coefficient R demand�')
        end
    else
        Nfft = 1024;
    end
else
    if Fentr ~= 0 % A la fois Nfft et la fen�tre sont sp�cifi�s, on v�rifie que les longueurs sont coh�rentes
        if length(Fentr)~= R*Nfft
            error('Dimensions de la fen�tre incompatible avec la longueur R*Nfft demand�e')
        end
    end
end
if nargin <1  % uniquement pour le debug, s'il n'y a pas de signal en entr�e !
    % Peut �tre mis en commentaire pour la release de la fonction
    x = exp(-2*1i*pi*(0:20*Nfft)*0.1234567);
end
if nargout > 2 % plusieur sorties, on doit calculer les cannaux
    demCan = 1;
else
    demCan = 0;
end
if nargout > 1 % on doit calculer le TF
    demTF = 1;
else % Une sortie, on ne calcule que le spectre
    demTF = 0;
end

[m,n] = size(x);
if n> m
    x = x.'; % Prend la transpos�e sans conjuguer
    [m,n] = size(x);
end
if (~(m >= Nfft) || ~(n >= 1) )
    error('Dimensions du signal incompatible avec longueur de DSP demand�e')
end


% R�servation des tableaux :
Dec = fix(Recouvrement * Nfft); % D�calage de chaque fen�tre de fft
nb_DSP = fix((m-R*Nfft+Dec)/Dec); % Nombre de fois o� on calcule une FFT
Spectre=zeros(Nfft,n);
if demTF
    A = zeros(Nfft,1);
    B = zeros(Nfft,1);
    IndMoyA = 1;
    if isinteger(NbMoy/2) % NbMoy est paire
        ValeurInitInd = 1;
        IndMoyB = 1-NbMoy/2;
        PasTF = NbMoy*Dec*NbMoy/2;
        nb_TF = 1 + fix( (nb_DSP-NbMoy)/(NbMoy/2) );
    else % NbMoy est impaire
        ValeurInitInd = 0;
        IndMoyB = -(NbMoy-1)/2;
        PasTF = NbMoy*Dec*(NbMoy+1)/2;
        nb_TF = 1 + fix( (nb_DSP-NbMoy)/((NbMoy+1)/2) );
    end
    TF = zeros(Nfft,nb_TF);
    IndTF = 1;
end
if demCan
    Cannaux = zeros(Nfft,nb_DSP,n);
end

% Calcul de la fen�tre de pond�ration
if Fentr == 0 % La fen�tre n'est pas sp�cifi�e, on utilise par d�faut Kaiser
    Beta = 0.1102*(Niv_Rejection-8.4); % Calcul de beta
    Fentr = kaiser(R*Nfft,Beta);
    norme = ( sum(Fentr) );
    Fentr = Fentr / norme ;
end
fnt = zeros(R*Nfft,n);
for k = 1:n
    fnt(:,k) = Fentr;
end

% D�calage initial en fr�quence si demand� :
if DecFreq ~=0
    for ind = 1:n
        x(:,ind) = x(:,ind) .* exp(2*1i*pi*DecFreq*(0:m-1)') ;
    end
end

%%%%%%%%%%%%%%% CALCUL %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for cpt = 1:nb_DSP
    nd = ((cpt-1) * Dec ) +1;
    nf = nd + R*Nfft-1;
    Segment = fnt .* x(nd:nf,:);
    Temp = Segment(1:Nfft,:);
    for r = 2:R
        Temp = Temp + Segment(1+(r-1)*Nfft:r*Nfft,:);
    end
    FFT = fftshift( fft(Temp) );
    if demCan
        DecPhase = ((nd-1)*Dec*pi/Nfft)*(0:Nfft-1)'.*ones(Nfft,1) ;
        Cannaux(:,cpt,:) = FFT .* exp(-1i*DecPhase) ;
    end
    DSP = FFT .* conj(FFT);
    Spectre = Spectre + DSP ;
    if demTF
        if IndMoyA>0
            A = A + sum(DSP,2);
        end
        IndMoyA = IndMoyA+1;
        if IndMoyA>NbMoy
            TF(:,IndTF) = A;
            IndTF = IndTF+1 ;
            A = zeros(Nfft,1);
            IndMoyA = ValeurInitInd;
        end
        if IndMoyB>0
            B = B + sum(DSP,2);
        end
        IndMoyB = IndMoyB+1;
        if IndMoyB>NbMoy
            TF(:,IndTF) = B ;
            IndTF = IndTF+1 ;
            B = zeros(Nfft,1);
            IndMoyB = ValeurInitInd;
        end
    end
end
Spectre = Spectre/(nb_DSP);

if nargout > 3
    Axe_Temps = (0:nb_TF-1)*PasTF;
    Axe_Freq = fftshift(0:Nfft-1) + DecFreq ;
end

if nargout == 0 % Par de sortie, donc on affiche le spectre
    figure(NumFig) ;
    plot(10*log10(Spectre(:,1)));
end
