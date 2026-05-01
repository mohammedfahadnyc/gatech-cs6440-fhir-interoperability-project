package edu.gatech.hapifhir;

import junit.framework.AssertionFailedError;

import java.util.ArrayList;
import java.util.List;

public class TestSummary {

    public interface TestExecutor { void execute() throws Throwable; }

    private static int total = 0;
    private static int passed = 0;
    private static int failed = 0;
    private static int errors = 0;
    private static final List<String> failMessages = new ArrayList<>();

    static {
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.out.println("\n=== SIMPLE TEST SUMMARY ===");
            System.out.println("Total tests run: " + total);
            System.out.println("Passed: " + passed);
            System.out.println("Failed (assertions): " + failed);
            System.out.println("Errors (exceptions): " + errors);
            if (!failMessages.isEmpty()) {
                System.out.println("\nFailures/Errors details:");
                for (String m : failMessages) System.out.println(" - " + m);
            }
            System.out.println("===========================\n");
        }));
    }

    public static void run(String testName, TestExecutor executor) throws Throwable {
        total++;
        try {
            executor.execute();
            passed++;
        } catch (AssertionFailedError afe) {
            failed++;
            String msg = testName + " - AssertionFailedError: " + afe.getMessage();
            failMessages.add(msg);
            System.out.println("TEST FAILED: " + msg);
            throw afe;
        } catch (Throwable t) {
            errors++;
            String msg = testName + " - Error: " + t.getClass().getSimpleName() + ": " + t.getMessage();
            failMessages.add(msg);
            System.out.println("TEST ERROR: " + msg);
            throw t;
        }
    }
}

