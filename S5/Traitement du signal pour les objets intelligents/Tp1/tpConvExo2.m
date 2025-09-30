clear all
close all
% Paramètres du signal sinusoïdal
f = 100; % Fréquence du signal
fe = 1000; % Fréquence d'échantillonnage
te = 1/fe; % Période d'échantillonnage
t = 0:te:1; % Intervalle de temps
% Génération du signal sinusoïdal (à compléter)
tabx = sin(2*pi*f*t);
% Filtre passe-bas de longueur 11 (à compléter)
N = 11;
tabh = ones(1,N)*1/3;
% Convolution (à compléter)
tabz = conv(tabx,tabh);
% Affichage
figure;
subplot(3,1,1);
plot(t, tabx);
title('Signal sinusoïdal tabx');
subplot(3,1,2);
plot(tabh);
title('Filtre passe-bas tabh');
subplot(3,1,3);
plot(t, tabz(1:length(t)));
title('Signal filtré tabz');