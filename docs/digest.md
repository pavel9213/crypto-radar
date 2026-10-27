# Signal digest

Crypto Radar can turn the latest collected JSON snapshot into a compact Markdown report.

Run it locally:

```sh
python scripts/build_digest.py
```

By default, it reads data/auto-news.json and writes data/latest-digest.md. Override either path with --feed or --output.

The digest contains update metadata, counts by confidence label and category, and up to 20 latest signals with source links. It is a reporting view of the existing feed, not a separate source of truth. Review the original linked announcement before treating a signal as actionable.
