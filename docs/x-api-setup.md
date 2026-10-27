# Optional X API setup

X monitoring is optional and depends on the access level and permissions of the X developer account.

1. Select an X developer app with access to the required recent-search endpoint.
2. Copy the bearer token from the developer console.
3. In GitHub, open repository Settings → Secrets and variables → Actions.
4. Add a repository secret named `X_BEARER_TOKEN`.
5. Trigger the feed workflow manually and inspect the run summary.
6. If requests fail, verify token validity, endpoint access, rate limits, and the current API plan.

Never put the token in `config/sources.json`, source code, issues, or committed logs. Rotate the secret if it is exposed.