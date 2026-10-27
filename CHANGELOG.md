# Changelog

Notable changes to Crypto Radar are recorded here.

## Unreleased

- Added unit tests for source-domain checks, RSS parsing, date normalization, and signal classification.
- Added a GitHub Actions test workflow for pushes, pull requests, and manual runs.
- Added a JSON Schema for the source configuration.
- Documented contribution, source-verification, and secret-handling practices.

## Initial collector

- Added scheduled collection from discoverable official RSS/Atom feeds.
- Added secondary Google News coverage with explicit unconfirmed/rumor labels.
- Added optional recent-post collection from configured X accounts when an API Bearer Token is supplied.
