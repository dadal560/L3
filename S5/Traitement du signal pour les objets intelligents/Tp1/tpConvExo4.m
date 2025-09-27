close all
clear all
f1 = 50;
f2 = 300;
te = 1/(10*f2); % Période d'échantillonnage
t = 0:te:1; % Intervalle de temps
% Génération du signal à deux fréquences sans bruit
tabxsansbruit = sin(2*pi*f1*t) + sin(2*pi*f2*t);
% Ajout de bruit blanc (à compléter)
tabx = tabxsansbruit + 0.3*randn(1,length(t))
% Filtre passe-bas (à compléter)
N = 7;
tabh = ones(1,N)*1/N;
% Convolution (à compléter)
tabz = conv(tabx,tabh);
% Affichage
figure;
subplot(3,1,1);
plot(t, tabx);
title('Signal bruité tabx');
subplot(3,1,2);
plot(tabh);
title('Filtre passe-bas tabh');
subplot(3,1,3);
plot(t, tabz(1:length(t)));
title('Signal filtré tabz');