function [SpectreCycl,C] = Cyclospectre(Signal1,Signal2,Npts,Nbt)
% algorithme de calcul des spectres cycliques de "Signal"
% Le nombre de points du spectre calculé est Npts 
% Signal2 est décalé par rapport à Signal1 de taux variant de 0 à Nbt
%
% "SpectreCycl" est le spectre cyclique calculé avec la somme de tous les
% spectre aux différents taux
% "C" est le tablau contenant tous les spectres cycliques pour chaque taux


[N1,n1] = size(Signal1);
[N2,n2] = size(Signal2);
N1=min(N1,N2);

% Nbt = 5 ; % Nombre de valeurs de tau

yy = zeros(N1-Nbt,Nbt+1);
for k=1:Nbt+1
    yy(:,k)= Signal1(1:N1-Nbt).* Signal2(k:N1-Nbt-1+k);
end

C = DSP(yy,Npts,80,0.25);
SpectreCycl =sum(C,2);




