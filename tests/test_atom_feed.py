"""Regression tests for Atom feed parsing."""
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("collect_news", ROOT / "scripts" / "collect_news.py")
collector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(collector)


class AtomFeedTests(unittest.TestCase):
    def test_atom_entry_uses_alternate_href(self):
        xml = b'''<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Snapshot update</title><link rel="alternate" href="https://example.org/snapshot"/><updated>2026-10-27T10:00:00Z</updated><summary>Eligibility information</summary></entry></feed>'''
        items = collector.parse_feed(xml)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "Snapshot update")
        self.assertEqual(items[0]["url"], "https://example.org/snapshot")
        self.assertEqual(items[0]["published_at"], "2026-10-27T10:00:00Z")

    def test_atom_entry_without_http_link_is_skipped(self):
        xml = b'''<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Unsafe</title><link href="javascript:alert(1)"/></entry></feed>'''
        self.assertEqual(collector.parse_feed(xml), [])


if __name__ == "__main__":
    unittest.main()
