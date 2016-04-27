function [Spectre,TF,nb_DSP,Nfft] = DSP(x,Nfft,Niv_Rejection,Recouvrement)
% Calcul la DSP du signal x ;
% EN ENTREE :
% x doit être un vecteur
% Les autres paramètres sont optionnelles.
% Nfft = nombre de points du spectre (Par defaut 1024 si pas spécifié)
% Niv_Rejection = niveau de réjection en dB (110 dB par défaut)
% Recouvrement : Chaque fenêtre de fft est décalée de NxRecouvrement
% par rapport à la fenêtre précédente (par défaut Recouvrement = 0.3)
% Utilise une fenètre de kaiser paramétrée pour avoir le niveau de
% réjection correspondant à Niv_Rejection
% La fenêtre est normalisée pour avoir un spectre de niveau  0 dB pour un
% signal CW de type exp(2*i*pi*freq*t) (c'est à dire une exponentiel
% complexe d'amplitude 1 )
% 
% EN SORTIE :
% Si il n'y a pas de sortie, DSP(x) affiche le spectre de x
% si non,
% Spectre est le spectre de puissance (DSP) du signal x
% TF est le diagramme temps/fréquence de l'énergie du signal x
% nb_DSP = est le nombre de DSP dans le TF (nombre de points sur l'axe
% temporel du diagramme temps/fréquence)
% Nfft est le nombre de fréquence dans le TF et le Spectre (nombre de
% points sur l'axe des fréquences dans le diagramme TF)
%
% EXEMPLE :
% Utilisation simplifiée : Sptr = DSP(Signal) (retourne dans Sptr le
% Spectre de DSP du vecteur Signal)

if nargin <4 % Si le recouvrement n'est pas spécifié par les paramètres d'entrées, 
    Recouvrement = 0.3; % recouvrement par défaut.
                        % Chaque fenêtre de fft est décalée de 0.3xN de la fenêtre précédente
end
if nargin <3 % Si la réjection n'est pas spécifiée par les paramètres d'entrées, 
    Niv_Rejection = 110; % 110 dB de réjection par defaut
end
if nargin <2 % Si le nombre de points de la fft n'est pas spécifié par les paramètres d'entrées, 
    Nfft = 1024;
end
if nargin <1  % uniquement pour le debug, s'il n'y a pas de signal en entrée !
    % Peut être mis en commentaire pour la release de la fonction
    x = exp(-2*i*pi*(0:2*Nfft)*0.1234567);
end
if nargout > 1 % plusieur sorties, on doit calculer le TF
    demTF = 1;
else % Une sortie, on ne calcule que le spectre
    demTF = 0;
end

[m,n] = size(x);
if n> m
    x = x';
    [m,n] = size(x);
end
if (~(m >= Nfft) || ~(n >= 1) )
    error('Dimensions du signal incompatible avec longueur de DSP demandée')
end


% Réservation des tableaux :
Dec = fix(Recouvrement * Nfft); % Décalage de chaque fenêtre de fft
nb_DSP = fix((m-Nfft+Dec)/Dec); % Nombre de fenêtres
Spectre=zeros(Nfft,n);
if demTF
    TF = zeros(Nfft,nb_DSP);
end

% Calcul de la fenêtre de pondération
Beta = 0.1102*(Niv_Rejection-8.4); % Calcul de beta
f = kaiser(Nfft,Beta);
norme = ( sum(f) );
f = f / norme ;
fnt = zeros(Nfft,n);
for k = 1:n
    fnt(:,k) = f;
end
for cpt = 1:nb_DSP
    nd = ((cpt-1) * Dec ) +1;
    nf = nd + Nfft-1;
    FFT = fft(fnt .* x(nd:nf,:));
    A = fftshift((FFT .* conj(FFT)));
    Spectre = Spectre + A ;
    if demTF
        TF(:,cpt) = sum(A,2);
    end
end
Spectre = Spectre/(nb_DSP);

if nargout == 0 % Par de sortie, donc on affiche le spectre
    figure(1)
    plot(10*log10(Spectre(:,1)));
end
