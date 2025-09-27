close all
clear all
% Fréquences du signal
f1 = 50;
f2 = 300;
te = 1/(10*f2); % Période d'échantillonnage
t = 0:te:1; % Intervalle de temps
% Génération du signal à deux fréquences (à compléter)
tabx = sin(2*pi*f1*t)+sin(2*pi*f2*t);
% Filtre passe-bas de longueur 7 (à compléter)
N = 7;
tabh = ones(1,N)*1/N;
% Convolution (à compléter)
tabz = conv(tabx,tabh);
% Affichage
figure;
subplot(3,1,1);
plot(t, tabx);
title('Signal à deux fréquences tabx');
subplot(3,1,2);
plot(tabh);
title('Filtre passe-bas tabh');
subplot(3,1,3);
plot(t, tabz(1:length(t)));
title('Signal filtré tabz');