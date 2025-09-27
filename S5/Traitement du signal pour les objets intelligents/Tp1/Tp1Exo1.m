f1 = 1e3;   % 1 kHz
f2 = 5e3;   % 5 kHz
t_end = 2;  % durée en secondes
A = 10;     % amplitude

fs = 10 * f2;      
t = 0:1/fs:t_end;  % vecteur temps

% signal 1: 1 kHz
x1 = A * sin(2*pi*f1*t);

% signal 2: 5 kHz
x2 = A * sin(2*pi*f2*t);

% affichage
figure('Name','Sinusoides 1kHz et 5kHz');
subplot(2,1,1);
plot(t(1:1000), x1(1:1000));
title('Sinusoide 1 kHz, A=10'); xlabel('t (s)'); ylabel('Amplitude'); grid on;

subplot(2,1,2);
plot(t(1:1000), x2(1:1000));
title('Sinusoide 5 kHz, A=10'); xlabel('t (s)'); ylabel('Amplitude'); grid on;
