# Crypto Radar

A lightweight, local-first Web3 watchlist for tracking crypto projects, news, TGE updates, snapshot chatter, airdrops, points, and source links.

## Features

- Project watchlist with search and category filters
- Signal feed with categories and clear status labels: Confirmed, Unconfirmed, Rumor, Monitoring
- Source URL and notes on every signal
- Add and remove projects and signals
- Export/import JSON backups
- Responsive dark UI; no build tools or runtime dependencies required
- Browser-local persistence for manual entries with `localStorage`
- GitHub Actions feed collector runs every four hours and can also be started manually
- Official RSS/Atom autodiscovery, Google News secondary coverage, source dates, and automatic rumor labels
- Optional official X account monitoring through the X API using a repository secret

## Run locally

Open `index.html` in a modern browser. For static hosting, publish the repository with GitHub Pages.

## Important limitations

- The scheduled collector writes `data/auto-news.json`; the page reads that file from GitHub Pages. The first run may take a few minutes after the workflow is enabled.
- Official feed posts and posts from configured official X handles are labeled `Confirmed` unless the text contains rumor/speculation language. This means the post comes from an official source, not that every claim in it has been independently audited.
- Google News search results are secondary coverage and are labeled `Unconfirmed`; items containing rumor/speculation wording are labeled `Rumor`. Their source link may point through Google News to the publisher.
- Official RSS feeds are discovered from project homepages where available. Some projects do not expose RSS, so add an `X_BEARER_TOKEN` secret for official X monitoring or configure a verified feed in `config/sources.json`.
- To enable X collection, create a repository secret named `X_BEARER_TOKEN` containing an X API Bearer Token with access to recent search. X API plan/permissions may be required. If the secret is absent, the rest of the collector still runs.
- GitHub Actions needs permission to write repository contents. Check **Settings → Actions → General → Workflow permissions** if the workflow cannot push the generated feed.
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
- Schedule: every four hours; you can also run it from **Actions → Update Crypto Radar feeds → Run workflow**.
- Collector: `scripts/collect_news.py`
- Source configuration: `config/sources.json`
- Generated data: `data/auto-news.json`
- Add or edit projects in `config/sources.json` to change keywords, official domains, websites, and X handles. Only list accounts/domains you have verified as official.

## Deploy with GitHub Pages

1. Open repository **Settings → Pages**.
2. Under build and deployment, choose **Deploy from a branch**.
3. Select `main` and `/ (root)`, then save.
4. Wait for GitHub Pages to publish the site; the URL will appear in the Pages settings.

## License

MIT
