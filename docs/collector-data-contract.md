# Collector data contract

The collector reads project definitions from `config/sources.json` and writes a generated feed to `data/auto-news.json`.

## Input expectations

Each project should have a stable lowercase ID, a display name, relevant keywords, official URLs/domains, and optional official X handles. Domains should identify the real publisher and should not be broad shared hosting domains.

## Output expectations

Each event should preserve a stable ID, project ID, display title, category, confidence label, date, source URL, source name/type, and a note that explains uncertainty when applicable. Timestamps should include timezone information.

## Compatibility

Treat the generated JSON as an interface consumed by the browser and digest generator. When changing field names or label values, update the validator, tests, and every consumer in the same change. Generated files should be changed by the workflow or generator rather than edited manually.