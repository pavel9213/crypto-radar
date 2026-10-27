# Architecture

Crypto Radar is a static browser application with a scheduled data collector.

## Data flow

1. `config/sources.json` defines project names, keywords, official domains, websites, and optional X handles.
2. `scripts/collect_news.py` discovers RSS/Atom feeds, reads secondary Google News results, and optionally queries recent posts from configured X accounts.
3. The collector normalizes items and assigns category and confidence labels.
4. The generated snapshot is written to `data/auto-news.json`.
5. GitHub Actions validates the snapshot and commits it when content changes.
6. The static page reads the generated snapshot; manual entries remain in browser `localStorage`.

## Trust boundaries

- Configured domains and X handles are allow-listed source metadata, not a guarantee that every statement is true.
- Secondary reporting must remain unconfirmed unless independently supported by a primary source.
- The X API token is read from the environment and should only be stored as a repository secret.
- The page escapes displayed text and only creates source links for HTTP(S) URLs.

## Design constraints

The collector uses the Python standard library so scheduled runs do not need a package-install step. Network requests have a timeout; unavailable sources should not prevent other projects from being processed.
