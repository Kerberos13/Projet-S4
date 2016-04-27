function PlotVisuSignal_2(handles,Signal,pathstr, name)

Ldsp = Signal.Ldsp ;
N = length(Signal.x);


% Axe Fréquentiel
axe_f = (0:Ldsp-1)*Signal.Fe/(Ldsp-1);
    
figure(handles);
TFlog = 10*log10(Signal.TF);
    Max = max(max(TFlog));
    Min = min(min(TFlog));
    TFlog = (TFlog-Min)*64/(Max-Min);
    NbPointTemp = size(TFlog,2);
    axe_t_TF = (0: NbPointTemp-1)*((N-1)/(Signal.Fe*(NbPointTemp-1)));
    ylabel('Temps / Freq');
    %coserver les axes
    image(axe_f,axe_t_TF, TFlog');
% conserver les axes :
%     tightInset = get(gca, 'TightInset');
%     position(1) = tightInset(1);
%     position(2) = tightInset(2);
%     position(3) = 1 - tightInset(1) - tightInset(3);
%     position(4) = 1 - tightInset(2) - tightInset(4);
%    set(gca, 'Position', position);

% version sans axes :
    set(gca,'position',[0 0 1 1],'units','normalized')
    axis off
    
    set(gcf,'PaperUnits','inches','PaperPosition',[0 0 4 3]);
    saveas(gca,[pathstr,'\',name, '.jpg'])
