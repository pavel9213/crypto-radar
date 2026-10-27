# Issue triage workflow

For each new issue:

1. Reproduce the behavior on the current default branch when possible.
2. Identify whether it affects the browser UI, source configuration, collector, validator, digest, or automation workflow.
3. Record the expected result and actual result separately.
4. Check for an existing issue or known limitation before opening a duplicate.
5. Assign severity based on user impact rather than implementation effort.
6. Add a regression test when the issue is caused by deterministic code behavior.
7. Close the issue only after verifying the fix or documenting why it will not be addressed.

Remove credentials, private wallet data, and personal information from screenshots and logs before sharing them.