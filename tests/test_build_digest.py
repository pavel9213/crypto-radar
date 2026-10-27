"""Tests for the Markdown digest generator."""
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_digest", ROOT / "scripts" / "build_digest.py")
digest = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(digest)


class DigestTests(unittest.TestCase):
    def test_empty_feed_has_clear_message(self):
        output = digest.build_digest({"updated_at": "2026-10-27T10:00:00Z", "events": []})
        self.assertIn("Total signals: **0**", output)
        self.assertIn("No signals are available yet.", output)

    def test_counts_categories_and_projects(self):
        payload = {"events": [
            {"id": "a", "projectId": "ink", "project": "Ink", "category": "TGE", "status": "Confirmed", "date": "2026-10-27", "publishedAt": "2026-10-27T10:00:00Z", "title": "Launch update", "source": "https://inkonchain.com/news"},
            {"id": "b", "projectId": "ink", "project": "Ink", "category": "Snapshot", "status": "Rumor", "date": "2026-10-26", "publishedAt": "2026-10-26T10:00:00Z", "title": "Snapshot chatter", "source": "https://inkonchain.com/post"}
        ]}
        output = digest.build_digest(payload)
        self.assertIn("Total signals: **2**", output)
        self.assertIn("Projects represented: **1**", output)
        self.assertIn("- Snapshot: 1", output)
        self.assertIn("- TGE: 1", output)
        self.assertIn("Rumors: **1**", output)

    def test_latest_items_appear_first(self):
        payload = {"events": [
            {"project": "Old", "category": "News", "status": "Unconfirmed", "date": "2026-01-01", "publishedAt": "2026-01-01T00:00:00Z", "title": "Older story", "source": "https://example.org/old"},
            {"project": "New", "category": "News", "status": "Confirmed", "date": "2026-10-27", "publishedAt": "2026-10-27T00:00:00Z", "title": "Newer story", "source": "https://example.org/new"}
        ]}
        output = digest.build_digest(payload)
        self.assertLess(output.index("Newer story"), output.index("Older story"))

    def test_non_http_source_is_not_rendered_as_link(self):
        payload = {"events": [{"project": "Test", "category": "News", "status": "Rumor", "date": "2026-10-27", "title": "Suspicious", "source": "javascript:alert(1)"}]}
        output = digest.build_digest(payload)
        self.assertNotIn("Source: <javascript:", output)


if __name__ == "__main__":
    unittest.main()
