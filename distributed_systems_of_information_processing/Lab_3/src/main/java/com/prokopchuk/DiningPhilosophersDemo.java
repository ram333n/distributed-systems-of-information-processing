package com.prokopchuk;

import java.util.concurrent.Semaphore;

public class DiningPhilosophersDemo {

    private final SolutionType solutionType;
    private final Philosopher[] philosophers;
    private final Fork[] forks;
    private Semaphore countingSemaphore;
    private Semaphore tableMutex;

    public static DiningPhilosophersDemo withOneCountingSemaphore(int philosophersCount) {
        DiningPhilosophersDemo result = new DiningPhilosophersDemo(philosophersCount, SolutionType.WITH_ONE_COUNTING_SEMAPHORE);
        initForTypeWithOneCountingSemaphore(result);

        return result;
    }

    private static void initForTypeWithOneCountingSemaphore(DiningPhilosophersDemo result) {
        int philosophersCount = result.philosophers.length;

        result.countingSemaphore = new Semaphore(philosophersCount - 1);

        for (int i = 0; i < philosophersCount; i++) {
            result.forks[i] = Fork.create(i);
        }

        for (int i = 0; i < philosophersCount; i++) {
            Fork leftFork = result.forks[i];
            Fork rightFork = result.forks[(i + 1) % philosophersCount];

            result.philosophers[i] = Philosopher.withOneCountingSemaphore(i, leftFork, rightFork, result.countingSemaphore);
        }
    }

    public static DiningPhilosophersDemo withForkAsMutex(int philosophersCount) {
        DiningPhilosophersDemo result = new DiningPhilosophersDemo(philosophersCount, SolutionType.WITH_FORK_AS_MUTEX);
        initForTypeWithForkAsMutex(result);

        return result;
    }

    private static void initForTypeWithForkAsMutex(DiningPhilosophersDemo result) {
        int philosophersCount = result.philosophers.length;

        result.tableMutex = new Semaphore(1);

        for (int i = 0; i < philosophersCount; i++) {
            result.forks[i] = Fork.create(i);
        }

        for (int i = 0; i < philosophersCount; i++) {
            Fork leftFork = result.forks[i];
            Fork rightFork = result.forks[(i + 1) % philosophersCount];

            result.philosophers[i] = Philosopher.withForkAsMutex(i, leftFork, rightFork, result.tableMutex);
        }
    }

    private DiningPhilosophersDemo(int philosophersCount, SolutionType solutionType) {
        this.solutionType = solutionType;
        this.philosophers = new Philosopher[philosophersCount];
        this.forks = new Fork[philosophersCount];
    }

    public void demo() {
        Thread[] threads = new Thread[philosophers.length];

        for (int i = 0; i < philosophers.length; i++) {
            threads[i] = new Thread(philosophers[i]);
        }

        for (Thread t : threads) {
            t.start();
        }
    }

}
