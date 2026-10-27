# Operations runbook

## Run collection manually

1. Open the repository's **Actions** tab.
2. Choose **Update Crypto Radar feeds**.
3. Select **Run workflow**.
4. Open the run and inspect the collector output.

## Expected behavior

- A run can finish successfully even when an individual feed is unavailable.
- The collector writes a complete JSON snapshot to `data/auto-news.json`.
- The workflow commits only when that file changes.
- If the X API secret is absent, RSS and secondary news collection still run.

## Troubleshooting

### The workflow cannot push

Check repository Actions permissions and branch protection rules. The workflow needs content write access to push the generated file.

### X results are missing

Confirm that `X_BEARER_TOKEN` is configured as a repository secret and that the API plan grants recent-search access. Never paste the token into logs or issues.

### The feed is empty

Inspect the source discovery output and the configured official URLs. Some websites do not publish RSS/Atom feeds; secondary search may also return no results.

### The feed JSON looks wrong

Run `python scripts/validate_data.py` and `python -m unittest discover -s tests -v` locally or inspect the test workflow.

## Recovery

If a generated snapshot is malformed, revert the offending commit and rerun the workflow after fixing the source or collector. Do not manually mark rumors as confirmed just to clear a warning.
