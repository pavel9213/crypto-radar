# Keyword taxonomy

The collector uses keyword rules to assign a primary category. Rules are heuristics and should be treated as a first-pass filter.

| Category | Typical signals | Review note |
| --- | --- | --- |
| TGE | token generation, token launch, listing date | Distinguish a plan from a confirmed date. |
| Snapshot | snapshot, eligibility checker | Check which network and activity period are meant. |
| Airdrop | airdrop, claim window, claim tokens | Discussion does not prove eligibility. |
| Points | points, XP, leaderboard | Points do not guarantee a future allocation. |
| Partnership | integration, collaboration, partner | Confirm both sides when possible. |
| News | general project updates | Use when no more specific rule matches. |
| Other | unmatched items | Inspect before changing taxonomy. |

When changing keywords, add regression tests for overlaps and rumor phrasing.