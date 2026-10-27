# Change review checklist

Before merging or publishing a change, ask:

- Does the change solve a clearly stated problem?
- Are source attribution and confidence labels still accurate?
- Are network failures handled without leaking credentials?
- Are input values validated before being used in URLs or output files?
- Are generated artifacts reproducible from the documented commands?
- Do tests cover the new behavior and a likely regression?
- Does the README still match the actual workflow?
- Are limitations documented instead of hidden?

If a check was not performed, report it as not performed rather than implying it passed.