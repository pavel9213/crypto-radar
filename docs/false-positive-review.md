# False-positive review

When an item is incorrectly categorized or labeled, capture its title, source URL, current label, expected label, and a short explanation.

Before changing the rules:

1. Check whether the item comes from an official or secondary source.
2. Identify which keyword caused the classification.
3. Consider whether the proposed rule would misclassify other categories.
4. Add a regression test for the original item and at least one nearby counterexample.
5. Keep source trust and claim truth separate.

Prefer a narrow rule with tests over a broad keyword that silently changes many existing items.