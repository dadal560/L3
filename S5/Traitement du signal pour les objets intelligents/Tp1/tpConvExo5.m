close all
clear all
f1 = 50;
f2 = 300;
te = 1/(10*f2); % Période d'échantillonnage
t = 0:te:1; % Intervalle de temps
% Génération du signal à deux fréquences sans bruit
tabxsansbruit = sin(2*pi*f1*t) + sin(2*pi*f2*t);
% Filtre passe-bas (à compléter)
N = 7;
tabh = ones(1,N)*1/N;
% Convolution (à compléter)
tabx = tabxsansbruit + 0.3*randn(1,length(t))
tabz = conv(tabx,tabh);
% FFT du signal sans bruit (à compléter)
X = fft(tabxsansbruit);
% Affichage du spectre du signal sans bruit
Nx=length(X);
figure;
fp = (0:Nx-1)/Nx/te;
fp = fp - 1/2/te;
stem(fp, fftshift(abs(X)));
axis([-1/(2*te) 1/(2*te) 0 max(abs(X))]);
xlabel('Fréquence (Hz)');
ylabel('Amplitude du spectre');
title('Spectre du signal sans bruit');
% FFT du signal filtré (à compléter)
Z = fft(tabz);
Nz=length(Z);
% Affichage du spectre du signal filtré
figure;
fp = (0:Nz-1)/Nz/te; 
fp = fp - 1/2/te;
stem(fp, fftshift(abs(Z)));
axis([-1/(2*te) 1/(2*te) 0 max(abs(Z))]);
xlabel('Fréquence (Hz)');
ylabel('Amplitude du spectre');
title('Spectre du signal filtré');