function [Spectre,TF,Cannaux,Axe_Temps,Axe_Freq] = DSP(x,Nfft,R,Niv_Rejection,Recouvrement,NbMoy,NumFig,DecFreq,Fentr)
%DSP spectre,temps/fréquence et canalisation
% Calcule la DSP du signal x ;
% Plus précisément, calcule le spectre de DSP, le diagramme temps/fréquence
% de la DSP et une canalisation du signal. Quelques informations
% suplémentaires sont également calculées.
%
% EXEMPLES D'UTILISATION :
% Sptr = DSP(Sig) (retourne dans Sptr le Spectre de Sig)
% [S,Dia] = DSP(Sig) (retourne le spectre et le diagramme temps fréquence)
% Sptr = DSP(Sig,4096) (Calcule le spectre avec des FFT de 4096 points)
% [S,Dia] = DSP(Sig,[],[],[],[],5) (calcul le diagramme temps
% fréquence avec un moyennage de 5 FFT pour chaque indice temporel)
% Seules les sorties demandées sont calculées et la plupart des entrées
% sont optionnelles.
% 
% EN ENTREE :
% x est soit un vecteur, soit un tableau. 
% Les autres paramètres sont optionnelles.
% Nfft = nombre de points du spectre (Par defaut 1024 si pas spécifié)
% R = nombre de longeur FFT additionnées dans le WOLA. R est entier >= à 1. 
% Si R=1, alors il n'y a qu'une seule longeur FFT utilisée et l'algorithme
% se réduit donc simplement à une fenêtre glissante. Si R >=2, on est donc
% avec un véritable WOLA. (par défaut R=1)
% Niv_Rejection = niveau de réjection en dB (110 dB par défaut)
% Recouvrement : Chaque fenêtre de fft est décalée de NxRecouvrement
% par rapport à la fenêtre précédente (par défaut Recouvrement = 0.3)
% NbMoy = nombre de spectre moyénné pour calculer une ligne du diagramme
% temps fréquence. (par défaut, NbMoy=1) NbMoy est entier >= à 1.
% NumFig : numéro de la figure où sera affiché le spectre, si affichage
% DecFreq = décalage en fréquence appliqué sur le signal. Ce paramètre
% permet de remettre les bin de FFT bien callé en fréquence sur  le centre
% des émissions attendues (par défaut = 0). Spécifié en fréquence réduite : 
% si dF est le vrai décalage à appliquer en Hertz et si Fe est la fréquence
% d'échantillonnage, alors DecFreq = dF/Fe
% Fentr : permet de spécifier la fenêtre a utiliser. Par défaut, la
% fonction utilise une fenêtre de Kaiser. Si on veut utiliser une autre
% fenêtre, il faut la communiquer à la fonction dans Fentr. La longueur de
% Fentr doit être égale à RxNfft. Si Fentr est utilisé, alors le paramètre 
% Niv_Rejection est sans effet.
%
% Utilise une fenètre de kaiser de longueur RxNfft et paramétrée pour avoir
% le niveau de réjection correspondant à Niv_Rejection
% La fenêtre est normalisée pour avoir un spectre de niveau  0 dB pour un
% signal CW de type exp(2*i*pi*freq*t) (c'est à dire une exponentiel
% complexe d'amplitude 1 )
% 
% EN SORTIE :
% Si il n'y a pas de sortie, DSP(x) affiche le spectre de x, dans la figure
% de numéro NumFig ou dans la fenêtre 1 si Numfig n'est pas spécifié
% si non,
% Spectre = le spectre de puissance (DSP) du signal x. Si x est un tableau,
% alors Spectre est un tableau dont chaque colone est la DSP d'un signaux
% de x
% TF = diagramme temps/fréquence de l'énergie du signal x. Si x est un
% tableau, alors on cumul toutes les puissances des signaux de x pour 
% construitre le diagramme TF
% Cannaux = signal canalisé
% Axe_Temps = vecteur contenant l'instant, en nombre d'échantillons, des  
% indices temporels du diagramme TF. Si Fe est la fréquence d'échantillonnage en
% Hertz, alors Axe_Temps/Fe est l'axe temporel en seconde.
% Axe_Freq = vecteur contenant les fréquences des bins. Les fréquences sont
% indiquées en fréquence réduite : si Fe est la fréquence
% d'échantillonnage, alors Axe_Freq*Fe sont les fréquences en Hertz.

if (nargin < 9)|| isempty(Fentr) % Si la fenêtre n'est pas spécifiée, 
    Fentr = 0; % 
end
if (nargin <8)||isempty(DecFreq) % Si pas de décalage en fréquence de spécifié, 
    DecFreq = 0; % le décalage est nul
end
if (nargin <7)||isempty(NumFig) % Si la figure n'est pas spécifié par les paramètres d'entrées, 
    NumFig = 1; % on utilise la figure n° 1.
end
if (nargin <6)||isempty(NbMoy) % Si la moyenne n'est pas spécifié par les paramètres d'entrées, 
    NbMoy = 1; %  par défaut pas de moyennage.
end
if (nargin <5)||isempty(Recouvrement) % Si le recouvrement n'est pas spécifié par les paramètres d'entrées, 
    Recouvrement = 0.3; % recouvrement par défaut.
                        % Chaque fenêtre de fft est décalée de 0.3xN de la fenêtre précédente
end
if (nargin <4)||isempty(Niv_Rejection) % Si la réjection n'est pas spécifiée par les paramètres d'entrées, 
    Niv_Rejection = 110; % 110 dB de réjection par defaut
end
if (nargin <3)||isempty(R) % Si la réjection n'est pas spécifiée par les paramètres d'entrées, 
    R = 1; % donc par defaut pas de WOLA  mais simplement une FFT glissante
end
if (nargin <2)||isempty(Nfft) % Si le nombre de points de la fft n'est pas spécifié par les paramètres d'entrées, 
    if Fentr ~= 0 % La fenêtre est spécifiée, mais pas Nfft
        Nfft = length(Fentr) / R ;
        if ~isinteger(Nfft)
            error('Dimensions de la fenêtre incompatible avec le coefficient R demandé')
        end
    else
        Nfft = 1024;
    end
else
    if Fentr ~= 0 % A la fois Nfft et la fenêtre sont spécifiés, on vérifie que les longueurs sont cohérentes
        if length(Fentr)~= R*Nfft
            error('Dimensions de la fenêtre incompatible avec la longueur R*Nfft demandée')
        end
    end
end
if nargin <1  % uniquement pour le debug, s'il n'y a pas de signal en entrée !
    % Peut être mis en commentaire pour la release de la fonction
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
    x = x.'; % Prend la transposée sans conjuguer
    [m,n] = size(x);
end
if (~(m >= Nfft) || ~(n >= 1) )
    error('Dimensions du signal incompatible avec longueur de DSP demandée')
end


% Réservation des tableaux :
Dec = fix(Recouvrement * Nfft); % Décalage de chaque fenêtre de fft
nb_DSP = fix((m-R*Nfft+Dec)/Dec); % Nombre de fois où on calcule une FFT
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

% Calcul de la fenêtre de pondération
if Fentr == 0 % La fenêtre n'est pas spécifiée, on utilise par défaut Kaiser
    Beta = 0.1102*(Niv_Rejection-8.4); % Calcul de beta
    Fentr = kaiser(R*Nfft,Beta);
    norme = ( sum(Fentr) );
    Fentr = Fentr / norme ;
end
fnt = zeros(R*Nfft,n);
for k = 1:n
    fnt(:,k) = Fentr;
end

% Décalage initial en fréquence si demandé :
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
