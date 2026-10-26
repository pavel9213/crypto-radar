# Crypto Radar

A lightweight, local-first Web3 watchlist for tracking crypto projects, news, TGE updates, snapshot chatter, airdrops, points, and source links.

## Features

- Project watchlist with search and category filters
- Signal feed with categories and clear status labels: Confirmed, Unconfirmed, Rumor, Monitoring
- Source URL and notes on every signal
- Add and remove projects and signals
- Export/import JSON backups
- Responsive dark UI; no build tools or dependencies required
- Browser-local persistence with `localStorage`

## Run locally

Open `index.html` in a modern browser. For static hosting, publish the repository with GitHub Pages.

## Important limitations

- This is a starter app. It **does not fetch live news**, verify claims automatically, connect a wallet, or use a backend.
- Seed entries are watch reminders, not claims that an event has happened or a token launch date is confirmed.
- Data is stored in the browser used to open the app. Export a JSON backup before clearing browser data or switching devices.
- Always verify TGE dates and snapshot announcements against official primary sources. Community posts and rumors are not confirmation.

## Tracked starter projects

- [Ink](https://inkonchain.com/) · [X](https://x.com/inkonchain)
- [Soneium](https://soneium.org/) · [X](https://x.com/soneium)
- [Base](https://www.base.org/)
- [Malda](https://malda.xyz/)
- [Rhuna](https://rhuna.io/)

## Deploy with GitHub Pages

1. Open repository **Settings → Pages**.
2. Under build and deployment, choose **Deploy from a branch**.
3. Select `main` and `/ (root)`, then save.
4. Wait for GitHub Pages to publish the site; the URL will appear in the Pages settings.

## License

MIT
