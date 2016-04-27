function [fi,moyfi,Histo_FI]=CalculFi(y,Fe,interp,a,seuil)
% fonction de calcul de la fréquence instantanée

[N,Bidon] = size(y);
phi = zeros(N-1,1);
fi = zeros(N,1);

phi = angle(y(2:N).* conj(y(1:N-1)));

fi(1)=2*phi(1);
fi(2:N-1) = phi(2:N-1)+phi(1:N-2);
fi(N)=2*phi(N-1);


if (nargin==5)&&(interp==1)
    selection=find((a(1:N-2)>seuil).*(a(2:N-1)>seuil).*(a(3:N)>seuil));
    selection=[1;selection+1;N];
    
    fiSel=fi(selection);
    fi=interp1(selection,fiSel,[1:N]','linear');
end;

fi = fi * Fe / (4*pi);
moyfi=mean(fi);
% fi = fi - moyfi;

%fi = real(fi);

Maxfi = max(fi);
Minfi = min(fi);
Paxfi = (Maxfi-Minfi)/256;
Histo_FI = histc(fi,(Minfi:Paxfi:Maxfi));
