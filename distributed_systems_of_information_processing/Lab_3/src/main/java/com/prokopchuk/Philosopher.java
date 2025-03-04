package com.prokopchuk;

import java.util.concurrent.Semaphore;
import lombok.Getter;

@Getter
public class Philosopher implements Runnable {

    private final int id;
    private final Fork leftFork;
    private final Fork rightFork;
    private final SolutionType type;
    private Semaphore semaphore;

    public static Philosopher withOneCountingSemaphore(int id, Fork leftFork, Fork rightFork, Semaphore semaphore) {
        return new Philosopher(id, leftFork, rightFork, SolutionType.WITH_ONE_COUNTING_SEMAPHORE, semaphore);
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
        //TODO: impl
    }

    private void solutionWithForkAsMutex() {
        //TODO: impl
    }

}
