# Contributing to Crypto Radar

Thanks for helping improve Crypto Radar.

## Before changing code

- Keep the collector dependency-free unless a new dependency has a clear benefit.
- Never commit API tokens, cookies, or other credentials.
- Keep automatically collected items linked to their original source.
- Treat secondary reporting as unconfirmed until an official project source confirms it.
- Do not label a claim confirmed merely because it is repeated by several secondary sites.

## Adding a project

1. Verify the project's official website and account links independently.
2. Add the project to `config/sources.json`.
3. Use the narrowest practical official domain; avoid broad hosting domains.
4. Add relevant keywords that distinguish the project from unrelated names.
5. Add or update tests if the configuration or classification behavior changes.

## Tests

Run the standard-library test suite from the repository root:

```sh
python -m unittest discover -s tests -v
```

The same command runs in GitHub Actions on pushes and pull requests.

## Pull requests

Explain the user-visible behavior change, include test results, and note any known limitations. Keep unrelated changes in separate commits when practical.
