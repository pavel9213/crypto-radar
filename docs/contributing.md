# Contributing

Small, focused changes are easier to review and safer to ship.

Before opening a change:

- Explain the user problem being solved.
- Keep source links and confidence labels honest.
- Add or update tests for logic changes.
- Run `python -m unittest discover -s tests -v`.
- Run `python scripts/validate_data.py` when configuration or generated data changes.
- Update documentation when behavior changes.
- Never commit secrets or wallet credentials.

Bug reports should include reproducible steps, expected behavior, actual behavior, and relevant browser or workflow details. Remove tokens and personal information from logs.