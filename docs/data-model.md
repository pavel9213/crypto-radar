# Automated event data contract

The collector writes a JSON object containing `updated_at`, `source_mode`, and an `events` array.

Each event includes:

| Field | Meaning |
| --- | --- |
| `id` | Stable identifier derived from project ID and source URL |
| `projectId` | ID matching a configured project |
| `project` | Human-readable project name |
| `category` | TGE, Snapshot, Airdrop, Points, Partnership, or News |
| `title` | Sanitized headline or official post text |
| `status` | Confirmed, Unconfirmed, or Rumor |
| `date` | UTC calendar date in ISO format |
| `publishedAt` | ISO-8601 timestamp with timezone when known |
| `source` | Original HTTP(S) source URL |
| `sourceName` | Publisher or configured account |
| `sourceType` | Source collection path, such as official or news-index |
| `automatic` | True for collector-generated items |
| `notes` | Short explanation of source confidence |

IDs should remain stable across runs so the UI can avoid displaying duplicates. Missing publication dates fall back to collection time and should be interpreted cautiously.
