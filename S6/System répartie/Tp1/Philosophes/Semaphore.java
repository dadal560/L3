package Tp1.Philosophes;

public class Semaphore {
    private int value;

    public Semaphore(int initial) {
        value = initial;
    }

    public synchronized void V() {
        ++value;
        notify();
    }// V

    public synchronized void P() {
        try {
            while (value == 0) wait();
        } catch (InterruptedException e) {}
        --value;
    }// P
}