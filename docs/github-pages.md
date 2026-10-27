# GitHub Pages deployment

Crypto Radar is a static site and can be hosted without a server-side application.

- Ensure the repository's Pages source points to the intended branch and folder.
- Confirm `index.html` is at the published root.
- Keep relative paths for repository-hosted JSON and assets where possible.
- Open the published page and check browser developer tools for missing assets or JSON requests.
- Remember that a local `file://` preview and a hosted HTTPS page can behave differently.
- If the feed appears stale, inspect Actions and the published `data/auto-news.json` before debugging the UI.

Publishing the page does not itself run the scheduled collector.