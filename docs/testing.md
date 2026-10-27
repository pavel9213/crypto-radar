# Testing and validation

Crypto Radar intentionally keeps its automated checks dependency-free.

## Run all unit tests

```sh
python -m unittest discover -s tests -v
```

## Validate configuration and feed output

```sh
python scripts/validate_data.py
```

The validator checks JSON readability, unique project/event IDs, HTTP(S) URLs, allowed status/category labels, date formats, timezone-aware timestamps, and key configuration fields.

## Validate after changing the collector

1. Add a focused unit test for the behavior.
2. Run the complete test suite.
3. Run the JSON validator against the current configuration and generated feed.
4. Review the diff to ensure source links and confidence labels remain correct.

GitHub Actions runs the test suite on pushes and pull requests. The scheduled feed workflow also validates the generated snapshot before committing it.
