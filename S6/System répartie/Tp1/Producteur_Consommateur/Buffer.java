package Tp1.Producteur_Consommateur;

public class Buffer {
    private int size;
    double[] buffer = new double[size];
    private int in = 0;    // dépôt 
    private int out = 0;   // retrait 

    private Semaphore vide;       // Compte les places libres
    private Semaphore plein;      // Compte les messages disponibles
    
    private Semaphore mutexProd;  // Pour les producteurs entre eux
    private Semaphore mutexConso; // Pour les consommateurs entre eux

    public Buffer(int size) {
        this.size = size;
        this.buffer = new double[size];

    
        this.vide = new Semaphore(size); // Initialisé à size (tout est vide au début)
        this.plein = new Semaphore(0); // Initialisé à 0 (rien à lire)
        
        // initialisés à 1 
        this.mutexProd = new Semaphore(1);
        this.mutexConso = new Semaphore(1);
    }

    public void depot(double value) {
        vide.P();          // Attente d'une place libre
        
        mutexProd.P();     // Exclusion mutuelle entre producteurs
        
        buffer[in] = value;
        in = (in + 1) % size; // Gestion circulaire 
        
        mutexProd.V();     // Fin exclusion mutuelle producteurs
        
        plein.V();         // Signale qu'un message est disponible
    }

    public double retrait() {
        double value = 0;
        plein.P();         // Attente d'un message
        
        mutexConso.P();    // Exclusion mutuelle entre consommateurs
        
        value = buffer[out];
        out = (out + 1) % size; // Gestion circulaire 
        
        mutexConso.V();    // Fin exclusion mutuelle consommateurs
        
        vide.V();          // Signale qu'une place est libérée
        return value;
    }
}