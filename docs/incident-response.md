# Incident response

Use this checklist if the collector or published feed behaves unexpectedly.

1. Open the latest run in GitHub Actions and identify the first failing step.
2. Check whether the failure is a network timeout, upstream format change, validation error, or Git commit permission issue.
3. Inspect the generated JSON diff before accepting automated output.
4. Keep the last known-good feed if a new run produces malformed or clearly degraded data.
5. Fix the cause and add a regression test when the failure can recur.
6. Re-run the workflow manually and verify both the feed and digest.
7. Record persistent upstream outages in the relevant documentation.

Do not add API tokens or other secrets to logs, issue reports, or committed files.