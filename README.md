# Crypto Radar

A lightweight, local-first Web3 watchlist for tracking crypto projects, news, TGE updates, snapshot chatter, airdrops, points, and source links.

## Features

- Project watchlist with search and category filters
- Signal feed with categories and confidence labels: Confirmed, Unconfirmed, Rumor, Monitoring
- Source URL and notes on every signal
- Add and remove projects and signals
- Export/import JSON backups
- Responsive dark UI; no build tools or runtime dependencies required
- Browser-local persistence for manual entries with `localStorage`
- GitHub Actions feed collector runs every four hours and can also be started manually
- Official RSS/Atom autodiscovery, Google News secondary coverage, normalized dates, and rumor labels
- Optional official X account monitoring through the X API using a repository secret
- Dependency-free unit tests and a validator for source configuration and generated feed data

## Run locally

Open `index.html` in a modern browser. For static hosting, publish the repository with GitHub Pages.

## Test and validate

Run the test suite:

```sh
python -m unittest discover -s tests -v
```

Validate the project source configuration and generated feed:

```sh
python scripts/validate_data.py
```

The tests run through GitHub Actions on pushes and pull requests. The scheduled feed workflow validates the generated JSON before committing it.

## Important limitations

- The scheduled collector writes `data/auto-news.json`; the page reads that file from GitHub Pages. The first run may take a few minutes after the workflow is enabled.
- Official feed posts and posts from configured official X handles are labeled `Confirmed` unless the text contains rumor/speculation language. This describes source origin, not independent verification of every claim.
- Google News results are secondary coverage and are labeled `Unconfirmed`; items containing rumor/speculation wording are labeled `Rumor`. Their source link may point through Google News to the publisher.
- Official RSS feeds are discovered from project homepages where available. Some projects do not expose RSS, so configure a verified feed or set the optional `X_BEARER_TOKEN` repository secret.
- X API access and recent-search permissions depend on the current API plan. If the secret is absent, the rest of the collector still runs.
- GitHub Actions needs permission to write repository contents for the feed workflow. Check **Settings → Actions → General → Workflow permissions** if it cannot push the generated feed.
- Manual entries remain in the browser where they were created. Export a JSON backup before clearing browser data or switching devices.
- Always verify TGE dates and snapshot announcements against official primary sources. No automated classifier can guarantee that a headline is true.

## Tracked starter projects

- [Ink](https://inkonchain.com/) · [X](https://x.com/inkonchain)
- [Soneium](https://soneium.org/) · [X](https://x.com/soneium)
- [Base](https://www.base.org/)
- [Malda](https://malda.xyz/)
- [Rhuna](https://rhuna.io/)

## Automated collection

- Workflow: [Update Crypto Radar feeds](.github/workflows/update-feeds.yml)
- Test workflow: [Test Crypto Radar](.github/workflows/tests.yml)
- Schedule: every four hours; start manually from **Actions → Update Crypto Radar feeds → Run workflow**.
- Collector: `scripts/collect_news.py`
- Validator: `scripts/validate_data.py`
- Source configuration: `config/sources.json`
- Generated data: `data/auto-news.json`
- Configuration schema: `config/sources.schema.json`
- Add or edit projects in `config/sources.json` to change keywords, official domains, websites, and X handles. Only list accounts/domains you have verified as official.

## Contributor documentation

- [Architecture](docs/architecture.md)
- [Adding a project](docs/adding-projects.md)
- [Signal labels](docs/signal-labels.md)
- [Data model](docs/data-model.md)
- [Testing](docs/testing.md)
- [Operations runbook](docs/operations.md)
- [Signal triage checklist](docs/triage-checklist.md)
- [Known limitations](docs/known-limitations.md)
- [Release checklist](docs/release-checklist.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Code of conduct](CODE_OF_CONDUCT.md)
- [Changelog](CHANGELOG.md)

## Deploy with GitHub Pages

1. Open repository **Settings → Pages**.
2. Under build and deployment, choose **Deploy from a branch**.
3. Select `main` and `/ (root)`, then save.
4. Wait for GitHub Pages to publish the site; the URL will appear in the Pages settings.

## License

MIT
