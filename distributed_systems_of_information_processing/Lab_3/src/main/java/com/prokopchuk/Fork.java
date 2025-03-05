package com.prokopchuk;

import java.util.concurrent.Semaphore;

public class Fork {

    private final int id;
    private final SolutionType solutionType;
    private final Semaphore mutex;

    public static Fork create(int id) {
        return new Fork(id, SolutionType.WITH_ONE_COUNTING_SEMAPHORE, new Semaphore(1));
    }

    private Fork(int id, SolutionType solutionType, Semaphore mutex) {
        this.id = id;
        this.solutionType = solutionType;
        this.mutex = mutex;
    }

    public void acquire() {
        try {
            mutex.acquire();
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

    public void release() {
        mutex.release();
    }

}
