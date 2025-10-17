clear all
close all
signales = load("double_tapMat.dat");
temp = signales(:, 1);

figure
for i = 2:9
    signale = signales(:, i);
    subplot(8,1,i-1)
    plot(temp,signale)
end

signales2 = load("fistMat.txt");
temp2 = signales2(:, 1);

figure
for i = 2:9
    signale = signales2(:, i);
    subplot(8,1,i-1)
    plot(temp2,signale)
end

figure 
subplot(2,1,1)
plot(temp,signales(:, 9))
subplot(2,1,2)
plot(temp2,signales2(:, 9))


figure 
enveloppe1 = abs(signales(:, 9)); 
enveloppe2 = abs(signales2(:, 9));

S1 = 0.5;
S2 = 0.5;

N = 80;
tabh = ones(1,N)*1/N;
tab1 = conv(enveloppe1, tabh, 'same');
tab2 = conv(enveloppe2, tabh, 'same');

tab1_clean = tab1;

tab2_clean = tab2;

hauteur_ligne = 12; 

activation_1 = tab1 > S1;
activation_2 = tab2 > S2; 

ligne_activation_1 = activation_1 * hauteur_ligne; 
ligne_activation_2 = activation_2 * hauteur_ligne;


subplot(2,1,1)
plot(temp,tab1,'r')
ylim([0.5 15])
hold on; 
plot(temp, ligne_activation_1, 'g'); 
hold off;
subplot(2,1,2)
plot(temp2,tab2,'r')
ylim([0.5 15])
hold on; 
plot(temp2, ligne_activation_2, 'g'); 
hold off;

figure
subplot(6,1,1)
plot(temp2,signales2(:, 9))
subplot(6,1,2)
signal_brut = signales2(:, 9);
T_DEBUT = 20; 
T_FIN = 63;   
signal_interesse = signal_brut;
indices_avant = temp2 < T_DEBUT;
signal_interesse(indices_avant) = 0;
indices_apres = temp2 > T_FIN;
signal_interesse(indices_apres) = 0;
plot(temp2, signal_interesse, 'm');