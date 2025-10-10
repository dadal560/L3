close all
clear all
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
plot(temp,signales(:, 2))
subplot(2,1,2)
plot(temp2,signales2(:, 2))


figure 
N = 11;
tabh = ones(1,N)*1/N;
tabz = conv(signales(:, 2), tabh, 'same');
subplot(2,1,1)
plot(temp,tabz)
tabe = conv(signales2(:, 2), tabh, 'same');
subplot(2,1,2)
plot(temp2,tabe)
