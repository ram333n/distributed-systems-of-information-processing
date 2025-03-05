package com.prokopchuk;

import java.security.SecureRandom;
import java.util.concurrent.Semaphore;
import lombok.Getter;

@Getter
public class Philosopher implements Runnable {

    private static final SecureRandom SECURE_RANDOM = new SecureRandom();
    private final int id;
    private final Fork leftFork;
    private final Fork rightFork;
    private final SolutionType type;
    private Semaphore semaphore; // table semaphore

    public static Philosopher withOneCountingSemaphore(int id, Fork leftFork, Fork rightFork, Semaphore semaphore) {
        return new Philosopher(id, leftFork, rightFork, SolutionType.WITH_ONE_COUNTING_SEMAPHORE, semaphore);
    }

    public static Philosopher withForkAsMutex(int id, Fork leftFork, Fork rightFork, Semaphore semaphore) {
        return new Philosopher(id, leftFork, rightFork, SolutionType.WITH_FORK_AS_MUTEX, semaphore);
    }

    private Philosopher(int id, Fork leftFork, Fork rightFork, SolutionType type) {
        this.id = id;
        this.leftFork = leftFork;
        this.rightFork = rightFork;
        this.type = type;
    }

    private Philosopher(int id, Fork leftFork, Fork rightFork, SolutionType type, Semaphore semaphore) {
        this(id, leftFork, rightFork, type);
        this.semaphore = semaphore;
    }

    @Override
    public void run() {
        switch (type) {
            case WITH_ONE_COUNTING_SEMAPHORE -> solutionWithOneCountingSemaphore();
            case WITH_FORK_AS_MUTEX -> solutionWithForkAsMutex();
            default -> throw new IllegalStateException("Unexpected solution type: " + type);
        }
    }

    private void solutionWithOneCountingSemaphore() {
        while (true) {
            think();
            acquireCountingAndForkSemaphores();
            eat();
            releaseCountingAndForkSemaphores();
        }
    }

    private void think() {
        try {
            System.out.printf("Philosopher: %d is thinking%n", id);
            Thread.sleep(2000L + SECURE_RANDOM.nextLong(500L));
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

    private void acquireCountingAndForkSemaphores() {
        try {
            semaphore.acquire();
            leftFork.acquire();
            rightFork.acquire();
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

    private void eat() {
        try {
            System.out.printf("Philosopher: %d is eating%n", id);
            Thread.sleep(1000L + SECURE_RANDOM.nextLong(500L));
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

    private void releaseCountingAndForkSemaphores() {
        leftFork.release();
        rightFork.release();
        semaphore.release();

        System.out.printf("Philosopher: %d finished eating%n", id);
    }

    private void solutionWithForkAsMutex() {
        while (true) {
            think();
            acquireTableAndForkSemaphores();
            eat();
            releaseTableAndForkSemaphores();
        }
    }

    private void acquireTableAndForkSemaphores() {
        try {
            semaphore.acquire();
            leftFork.acquire();
            rightFork.acquire();
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

    private void releaseTableAndForkSemaphores() {
        leftFork.release();
        rightFork.release();
        semaphore.release();

        System.out.printf("Philosopher: %d finished eating and released the table%n", id);
    }

}
