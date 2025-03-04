package com.prokopchuk;

import java.util.concurrent.Semaphore;

public class Fork {

    private final int id;
    private final SolutionType solutionType;
    private Semaphore mutex;

    public static Fork withOneCountingSemaphore(int id) {
        return new Fork(id, SolutionType.WITH_ONE_COUNTING_SEMAPHORE);
    }

    private Fork(int id, SolutionType solutionType) {
        this.id = id;
        this.solutionType = solutionType;
    }

}
