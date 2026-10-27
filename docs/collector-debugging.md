# Collector debugging guide

## Workflow fails before collection

Check the Python setup step, workflow permissions, and the first error in the Actions log.

## A project has no new items

Check whether its homepage exposes RSS or Atom, whether candidate feed URLs respond, and whether the source has published anything recently. A quiet project is not necessarily a broken collector.

## Items have wrong labels

Inspect the title and summary used by the keyword rules. Add a narrow regression test before changing a shared pattern.

## The output is rejected

Run `python scripts/validate_data.py` locally and fix the first reported schema issue. Do not bypass validation just to publish a run.

## The digest is stale

Confirm the workflow ran the digest builder after the collector and that `data/latest-digest.md` was included in the generated-data commit.

Never paste API secrets into issue reports or logs.