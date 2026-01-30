package Tp1.Philosophes;

public class Main {
    public static void main(String[] args) {
        System.out.println("Dîner des Philosophes: Début");
        
        int nb = 5;
        Semaphore[] f = new Semaphore[nb];

        // On crée les fourchettes
        for (int i = 0; i < nb; i++) {
            f[i] = new Semaphore(1);
        }

        // On crée les philosophes 
        for (int i = 0; i < nb; i++) {
            Semaphore gauche = f[i];
            Semaphore droite = f[(i + 1) % nb];

            if (i == nb - 1) {
                // Le dernier est inversé (Droite puis Gauche)
                new Philosophe(i, droite, gauche); 
            } else {
                // Les autres sont normaux (Gauche puis Droite)
                new Philosophe(i, gauche, droite);
            }
        }
        
        try { System.in.read(); } catch(Exception e) {}
    }
}