package Tp1.Producteur_Consommateur;

class Consommateur implements Runnable {
    Buffer b = null;
    int id = 0;
    public Consommateur(Buffer initb, int n) {
        b = initb;
        id = n;
        new Thread(this).start();
    }
    public void run() {
        double item;
        while (true) {
            System.out.println(" ---"+id+"---- DEMANDE" );
            item = b.retrait();
            System.out.println(" ---"+id+"---- A RETIRE "+ item);
            try { Thread.sleep(id * 500);}
            catch (Exception e){ };
        }
    }
}