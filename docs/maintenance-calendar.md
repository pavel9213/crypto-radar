# Maintenance calendar

## Every feed run

- Check workflow success and validator output.
- Inspect unexpected changes in item count.
- Verify the digest is generated from the same feed snapshot.

## Weekly

- Spot-check several newest source links.
- Review repeated duplicates and false-positive categories.
- Check whether configured official sites and social handles still belong to the intended projects.

## After code changes

- Run the full unittest suite.
- Run the data validator.
- Review generated output before committing it.
- Update documentation when a behavior or label changes.

A green workflow is a useful signal, not a substitute for checking the quality of collected claims.