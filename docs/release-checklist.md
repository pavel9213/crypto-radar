# Release readiness checklist

- [ ] Run `python -m unittest discover -s tests -v`.
- [ ] Run `python scripts/validate_data.py`.
- [ ] Inspect the collector diff for duplicate IDs and unexpected status changes.
- [ ] Confirm the automated feed contains valid HTTP(S) source links.
- [ ] Review source configuration changes for verified domains and accounts.
- [ ] Confirm no API tokens or environment files are included in the diff.
- [ ] Check mobile layout and keyboard navigation after UI changes.
- [ ] Update the README or changelog for user-visible changes.
- [ ] Confirm scheduled and manual workflows still have the required permissions.
- [ ] Verify deployment and role/achievement status in their respective dashboards; do not assume a successful commit guarantees external credit.
