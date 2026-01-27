package Tp1.Producteur_Consommateur;

public class Main {
    public static void main(String[] args) {
        Buffer buffer = new Buffer(10);
        
        new Producteur(buffer);

        new Consommateur(buffer, 1); 
        new Consommateur(buffer, 2); 
        try { 
            System.in.read(); }
        catch( Exception e ) { }
        System.exit(0);
    }
}