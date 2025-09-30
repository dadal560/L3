tabx = [1 1 1 1 2 2 2 2 1 1 1 1];
tabtempx = [0 0 1 1 1 2 2 2 2 1 1 1 1 0 0]
% Filtre passe-bas (à compléter)
tabh = [1/3,1/3,1/3];
% Convolution (à compléter)
tabz = conv(tabh,tabx);
% Affichage
figure(1);
subplot(3,1,1)
stem(tabtempx)
axis([0 length(tabtempx) 0 3])
subplot(3,1,2)
stem(tabh)
axis([0 length(tabtempx) 0 3])
subplot(3,1,3)
stem(tabz)% Filtre passe-bas de longueur 11 (à compléter) N = 11; tabh = __________;