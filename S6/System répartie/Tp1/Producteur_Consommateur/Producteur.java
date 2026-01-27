package Tp1.Producteur_Consommateur;

public class Producteur implements Runnable {
    Buffer b = null;
    public Producteur(Buffer initb) {
        b = initb;
        new Thread(this).start();
    }
    public void run() {
        double item;
        while (true) {
            item = Math.random() * 20.0;
            System.out.println("++ AJOUTE ++ " + item);
            b.depot(item);
            System.out.println("++ MIS ++ " + item);
            try { Thread.sleep(200);}
            catch (Exception e){ } ;
        }
    }
}