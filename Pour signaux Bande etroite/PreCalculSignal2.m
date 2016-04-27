function S = PreCalculSignal2(x,Fe,Ldsp)

%%%%%%%%%
% CALCUL DES SIGNAUX DERIVES de x
%%%%%%%%%
xm = mean(x) ;
x = x-xm ;
coef = max(max(abs(real(x))),max(abs(imag(x)))) ;
x = x/coef ;
a = abs(x) ;
am = mean(a) ;
% a = a/am;
x = x/am;
% S.a = a;
% S.an = (a -mean(a))/mean(a);
S.x = x;
% a2 = a .* a;
S.Fe = Fe;
S.Ldsp = Ldsp;
% S.Lhisto = Lhisto;
% S.Lcyclo = Lcyclo ;
% S.Nbt = Nbt ;
% [S.FI, S.moyfi, S.Histo_FI]=CalculFi(x,S.Fe,0,a2,max(a2)/100);

%%%%%%%%%
% DSP de x x� x4 et x8
[S.DSP_X, S.TF] = DSP(x,S.Ldsp,90,0.25);
% X2 = x.*x;
% S.DSP_X2 = DSP(X2,S.Ldsp,90,0.25);
% X4 = X2.*X2 ;
% S.DSP_X4 = DSP(X4,S.Ldsp,90,0.25);
% X8 = X4.*X4 ;
% S.DSP_X8 = DSP(X8,S.Ldsp,90,0.25);
% clear X8
% S.DSPdB_X = 10*log10(S.DSP_X);

% % DSP de FI
% S.DSP_FI = DSP(S.FI,S.Ldsp,90,0.25);
% 
% % DSP de A
% S.DSP_A = DSP(S.an,S.Ldsp,90,0.25);
% 
% % DSP de A2
% S.DSP_A2 = DSP(S.an.^2,S.Ldsp,90,0.25);
% 
% % DSP de A4
% S.DSP_A4 = DSP(S.an.^4,S.Ldsp,90,0.25);
% 
% % DSP de A8
% S.DSP_A8 = DSP(S.an.^8,S.Ldsp,90,0.25);
% 
% % histogrammes   
% amax=max(a);
% SupportHistoAmp = (0 : amax/(S.Lhisto-1) : amax);
% S.HistoAmp = histc(a,SupportHistoAmp);

% % Cyclospectres :
% [S.Cyclo_XX, S.GrapheCyclo_XX] = Cyclospectre(S.x, S.x, S.Lcyclo, S.Nbt);
% [S.Cyclo_XXC, S.GrapheCyclo_XXC] = Cyclospectre(S.x, conj(S.x), S.Lcyclo, S.Nbt);
% [S.Cyclo_X2X2, S.GrapheCyclo_X2X2] = Cyclospectre(X2, X2, S.Lcyclo, S.Nbt);
% [S.Cyclo_X2X2C, S.GrapheCyclo_X2X2C] = Cyclospectre(X2, conj(X2), S.Lcyclo, S.Nbt);
% [S.Cyclo_FiFi, S.GrapheCyclo_FiFi] = Cyclospectre(S.FI, S.FI, S.Lcyclo, S.Nbt);
% 
% %%%%%%%%%
% % CALCUL DES SIGNAUX EN HYPOTHESE FM INDIRECTE
% %%%%%%%%%
% fih = hilbert(S.FI);
% fihm = mean(abs(fih));
% S.FIH = fih / fihm;
% [S.dfi,S.moydfi]=CalculFi(S.FI,S.Fe);
% 
% S.DSP_FIH = DSP(abs(S.FIH),S.Ldsp,90,0.25);
% [S.Cyclo_FihFihC, S.GrapheCyclo_FihFihC] =Cyclospectre(S.FIH, conj(S.FIH), S.Lcyclo, S.Nbt);
% 
% %%%%%%%%%
% % CALCUL DES SIGNAUX EN HYPOTHESE AM INDIRECTE
% %%%%%%%%%
% ah = hilbert(S.a);
% ahm = mean(abs(ah));
% S.ah = ah / ahm;
% 
% S.DSP_AH = DSP(abs(S.ah),S.Ldsp,90,0.25);
% [S.Cyclo_AhAhC, S.GrapheCyclo_AhAhC] =Cyclospectre(S.ah, conj(S.ah), S.Lcyclo, S.Nbt);

