package Tp1.Philosophes;

public class Philosophe implements Runnable {
    private int id;
    private Semaphore gauche;
    private Semaphore droite;

    public Philosophe(int id, Semaphore gauche, Semaphore droite) {
        this.id = id;
        this.gauche = gauche;
        this.droite = droite;
        new Thread(this).start();
    }

    public void run() {
        try {
            while (true) {
            
                System.out.println("Philosophe " + id + " pense.");
                Thread.sleep((long) (Math.random() * 500));

                System.out.println("Philosophe " + id + " a FAIM.");
                
                gauche.P();
                System.out.println("Philosophe " + id + " a pris GAUCHE (-1).");
                
                Thread.sleep(100); 
                
                droite.P();
                System.out.println("Philosophe " + id + " a pris DROITE (-1).");

                System.out.println("Philosophe " + id + " MANGE ");
                Thread.sleep((long) (Math.random() * 500));

                gauche.V();
                System.out.println("Philosophe " + id + " a rendu GAUCHE (+1).");
                droite.V();
                System.out.println("Philosophe " + id + " a rendu DROITE (+1).");
                
                System.out.println("Philosophe " + id + " a fini son cycle.");
            }
        } catch (InterruptedException e) {}
    }
}