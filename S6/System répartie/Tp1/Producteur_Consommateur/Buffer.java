package Tp1.Producteur_Consommateur;

public class Buffer {
    int size = 10;
    double[] buffer = new double[size];

    public Buffer(int n) {
        size = n;
    }

    public void depot(double value) {
    }

    public double retrait() {
        double value = 0;
        return value;
    }
}