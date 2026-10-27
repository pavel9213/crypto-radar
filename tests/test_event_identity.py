"""Tests for stable IDs and provenance in generated feed events."""
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("collect_news", ROOT / "scripts" / "collect_news.py")
collector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(collector)


class EventIdentityTests(unittest.TestCase):
    def setUp(self):
        self.project = {"id": "sample", "name": "Sample", "official_domains": ["example.org"]}
        self.item = {"title": "Snapshot checker", "url": "https://example.org/updates/", "published_at": "2026-10-27T12:00:00Z", "summary": "Eligibility update", "publisher": "Example"}

    def test_event_id_is_stable_for_same_project_and_url(self):
        first = collector.make_event(self.project, self.item, True, "official")
        second = collector.make_event(self.project, dict(self.item), True, "official")
        self.assertEqual(first["id"], second["id"])

    def test_trailing_slash_does_not_change_event_id(self):
        first = collector.make_event(self.project, self.item, True, "official")
        changed = dict(self.item, url="https://example.org/updates")
        second = collector.make_event(self.project, changed, True, "official")
        self.assertEqual(first["id"], second["id"])

    def test_secondary_event_preserves_uncertainty(self):
        event = collector.make_event(self.project, self.item, False, "news-index")
        self.assertEqual(event["status"], "Unconfirmed")
        self.assertIn("not an official confirmation", event["notes"])

    def test_rumor_event_explains_label(self):
        item = dict(self.item, title="Rumored snapshot checker")
        event = collector.make_event(self.project, item, True, "official")
        self.assertEqual(event["status"], "Rumor")
        self.assertIn("Treat as unconfirmed", event["notes"])


if __name__ == "__main__":
    unittest.main()
