# Privacy notes

Crypto Radar is a static watchlist. Manual entries are stored in the current browser profile using local storage; they are not automatically synchronized across devices.

The automated collector may fetch public RSS/Atom feeds, public pages for feed discovery, Google News RSS results, and optionally X API results when a repository secret is configured. Requests are made by the GitHub Actions runner, not by the visitor's browser.

Do not store passwords, private keys, wallet seed phrases, or personal access tokens in the watchlist. Keep API credentials in GitHub Actions secrets and rotate them if exposure is suspected.