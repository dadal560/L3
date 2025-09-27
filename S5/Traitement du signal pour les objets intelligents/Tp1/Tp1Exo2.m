donnees = load('data.dat');   


t_min = donnees(:,1);        
donnees_temp = donnees(:,2); 

t_jours = t_min / (60*24);

% Modèle 1 
m = 19.8;
a = 3;
T = 24;  
x1 = m + a*cos(2*pi*(t_min/60)/T);

% Modèle 2 
b = 1/(4*24);  
x2 = (m + b*(t_min/60)) + a*cos(2*pi*(t_min/60)/T);

subplot(3,1,1);
plot(t_jours, donnees_temp,"+");
xlabel('Temps (jours)'); 
ylabel('Température (°C)');
ylim([16,24])

subplot(3,1,2);
plot(t_jours, donnees_temp,"+",t_jours, x1);
xlabel('Temps (jours)'); 
ylabel('Température (°C)');
ylim([0,30])

subplot(3,1,3);
plot(t_jours, donnees_temp,"+",t_jours, x1,t_jours, x2);
legend('données','modèle 1','modèle 2')
xlabel('Temps (jours)'); 
ylabel('Température (°C)');
ylim([0,30])

d1 = norm(donnees_temp - x1);
d2 = norm(donnees_temp - x2);

fprintf('Distance modèle 1 : %.2f\n', d1);
fprintf('Distance modèle 2 : %.2f\n', d2);

erreur = d1 - d2;
fprintf('erreur : %.2f\n',erreur);
