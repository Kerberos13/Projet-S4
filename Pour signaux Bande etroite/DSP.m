function [Spectre,TF,nb_DSP,Nfft] = DSP(x,Nfft,Niv_Rejection,Recouvrement)
% Calcul la DSP du signal x ;
% EN ENTREE :
% x doit �tre un vecteur
% Les autres param�tres sont optionnelles.
% Nfft = nombre de points du spectre (Par defaut 1024 si pas sp�cifi�)
% Niv_Rejection = niveau de r�jection en dB (110 dB par d�faut)
% Recouvrement : Chaque fen�tre de fft est d�cal�e de NxRecouvrement
% par rapport � la fen�tre pr�c�dente (par d�faut Recouvrement = 0.3)
% Utilise une fen�tre de kaiser param�tr�e pour avoir le niveau de
% r�jection correspondant � Niv_Rejection
% La fen�tre est normalis�e pour avoir un spectre de niveau  0 dB pour un
% signal CW de type exp(2*i*pi*freq*t) (c'est � dire une exponentiel
% complexe d'amplitude 1 )
% 
% EN SORTIE :
% Si il n'y a pas de sortie, DSP(x) affiche le spectre de x
% si non,
% Spectre est le spectre de puissance (DSP) du signal x
% TF est le diagramme temps/fr�quence de l'�nergie du signal x
% nb_DSP = est le nombre de DSP dans le TF (nombre de points sur l'axe
% temporel du diagramme temps/fr�quence)
% Nfft est le nombre de fr�quence dans le TF et le Spectre (nombre de
% points sur l'axe des fr�quences dans le diagramme TF)
%
% EXEMPLE :
% Utilisation simplifi�e : Sptr = DSP(Signal) (retourne dans Sptr le
% Spectre de DSP du vecteur Signal)

if nargin <4 % Si le recouvrement n'est pas sp�cifi� par les param�tres d'entr�es, 
    Recouvrement = 0.3; % recouvrement par d�faut.
                        % Chaque fen�tre de fft est d�cal�e de 0.3xN de la fen�tre pr�c�dente
end
if nargin <3 % Si la r�jection n'est pas sp�cifi�e par les param�tres d'entr�es, 
    Niv_Rejection = 110; % 110 dB de r�jection par defaut
end
if nargin <2 % Si le nombre de points de la fft n'est pas sp�cifi� par les param�tres d'entr�es, 
    Nfft = 1024;
end
if nargin <1  % uniquement pour le debug, s'il n'y a pas de signal en entr�e !
    % Peut �tre mis en commentaire pour la release de la fonction
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
    error('Dimensions du signal incompatible avec longueur de DSP demand�e')
end


% R�servation des tableaux :
Dec = fix(Recouvrement * Nfft); % D�calage de chaque fen�tre de fft
nb_DSP = fix((m-Nfft+Dec)/Dec); % Nombre de fen�tres
Spectre=zeros(Nfft,n);
if demTF
    TF = zeros(Nfft,nb_DSP);
end

% Calcul de la fen�tre de pond�ration
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
