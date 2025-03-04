package com.prokopchuk;

public class Main {

    public static void main(String[] args) {
        final int philosophersCount = 5;
        DiningPhilosophersDemo demo = DiningPhilosophersDemo.withOneCountingSemaphore(philosophersCount);
        demo.demo();
    }

}