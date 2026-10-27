# Post-deployment smoke test

After publishing a new version:

1. Load the hosted page over HTTPS.
2. Confirm the page shell and project list appear.
3. Check that the generated feed JSON request succeeds.
4. Search for a known project and clear the search.
5. Apply and reset category/status filters.
6. Open a source link and verify its destination.
7. Add a harmless test entry in a disposable browser profile and confirm it survives refresh.
8. Check a narrow viewport for clipped controls and horizontal overflow.
9. Remove the test entry and confirm the profile is clean.

Record the browser, deployment URL, and any failed step in the release notes.