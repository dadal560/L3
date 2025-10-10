clear all;
close all;
tabx = [1 1 1 1 2 2 2 2 1 1 1 1];
tabtempx = [0 0 1 1 1 2 2 2 2 1 1 1 1 0 0];
N=3;
tabh = ones(1,N)*1/3;
function taby = convolution(tabx,tabh)
    ln = length(tabx);
    lh = length(tabh);
    tabtempx = [zeros(1, lh-1), tabx, zeros(1, lh-1)];
    taby = zeros(1, ln + lh - 1);
    for n = 1:(ln + lh - 1)
        for k = 1:lh
            taby(n) = taby(n) + tabh(k) * tabtempx(n+lh-k);
        end
    end
end


tabz = convolution(tabx,tabh);

disp(tabz)
 
figure(1);
subplot(3,1,1)
stem(tabtempx)
axis([0 length(tabtempx) 0 3])
subplot(3,1,2)
stem(tabh)
axis([0 length(tabtempx) 0 3])
subplot(3,1,3)
stem(tabz)