# Adding a tracked project

Edit `config/sources.json` and add one object to `projects`.

Required fields:

- `id`: stable lowercase slug, such as `sample-chain`.
- `name`: display name.
- `keywords`: phrases for secondary news search. Keep them specific enough to avoid unrelated results.
- `official_urls`: verified project homepages used for feed discovery.
- `official_domains`: exact official hostnames, without schemes or paths.
- `x_handles`: verified official X handles, without the @ symbol.

Example:

```json
{
  "id": "sample-chain",
  "name": "Sample Chain",
  "keywords": ["Sample Chain blockchain"],
  "official_urls": ["https://example.org/"],
  "official_domains": ["example.org"],
  "x_handles": ["sample_chain"]
}
```

The example domain and account are placeholders, not a recommendation to track them as real sources. Verify every source independently before using it. Then run the tests and validator.
