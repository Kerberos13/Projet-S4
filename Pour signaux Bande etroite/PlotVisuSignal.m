function PlotVisuSignal(handles,Signal)

Ldsp = Signal.Ldsp ;
N = length(Signal.x);

% Axe Temporel
axe_t = (0:N-1)/Signal.Fe;
% Axe Fréquentiel
axe_f = (0:Ldsp-1)*Signal.Fe/(Ldsp-1);
    
figure(handles);
subplot(5, 2, 1:2);
plot(axe_t, real(Signal.x), axe_t, imag(Signal.x));
    ylabel('I / Q (t) ');
    maxi = max(abs(real(Signal.x)));
    maxq = max(abs(imag(Signal.x)));
    dyn = max(maxi, maxq) ;
    axis([axe_t(1) axe_t(N) -1.1*dyn +1.1*dyn]);

subplot(5, 2, 3:4);
plot(axe_t, Signal.a);
    ylabel({'Puissance ';'Instantanée(t)'});
    maxx = max(Signal.a);
    minx= min(Signal.a);
    dyn = maxx-minx;
    axis([axe_t(1) axe_t(N) minx-0.1*dyn maxx+0.1*dyn]);

subplot(5, 2, 5:6);
plot(axe_t, Signal.FI);
    ylabel({'Fréquence';'Instantanée(t)'});
    dyn = max(abs(Signal.FI));
    axis([axe_t(1) axe_t(N) -1.1*dyn +1.1*dyn]);

subplot(5, 2, 7:8);
TFlog = 10*log10(Signal.TF);
    Max = max(max(TFlog));
    Min = min(min(TFlog));
    TFlog = (TFlog-Min)*64/(Max-Min);
    NbPointTemp = size(TFlog,2);
    axe_t_TF = (0: NbPointTemp-1)*((N-1)/(Signal.Fe*(NbPointTemp-1)));
    ylabel('Temps / Freq');
    %set(gcf,'CurrentAxes',handles.axes_TF) 
    image(axe_t_TF, axe_f, TFlog);
    saveas(gcf,'myfig.jpg')
subplot(5, 2, 9);
plot(Signal.DSPdB_X);
    ylabel('DSP');
    
subplot(5, 2, 10);
plot(Signal.Histo_FI);
    ylabel('Histo FI');
    
    
    