"""Unit tests for the Crypto Radar news collector (stdlib only)."""
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("collect_news", ROOT / "scripts" / "collect_news.py")
collector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(collector)


class ClassificationTests(unittest.TestCase):
    def test_tge_category(self):
        self.assertEqual(collector.category_for("Official TGE date announced"), "TGE")

    def test_snapshot_category(self):
        self.assertEqual(collector.category_for("Snapshot checker is now live"), "Snapshot")

    def test_airdrop_category(self):
        self.assertEqual(collector.category_for("Airdrop claim window opens Friday"), "Airdrop")

    def test_points_category(self):
        self.assertEqual(collector.category_for("Points leaderboard updated"), "Points")

    def test_partnership_category(self):
        self.assertEqual(collector.category_for("New ecosystem partnership"), "Partnership")

    def test_unknown_item_is_news(self):
        self.assertEqual(collector.category_for("Developer update"), "News")

    def test_official_source_is_not_automatically_truth_verified(self):
        self.assertEqual(collector.status_for("TGE announced", "", True), "Confirmed")

    def test_secondary_source_is_unconfirmed(self):
        self.assertEqual(collector.status_for("Possible launch date", "", False), "Unconfirmed")

    def test_rumor_language_overrides_source_type(self):
        self.assertEqual(collector.status_for("Rumored token launch", "", True), "Rumor")

    def test_british_and_american_rumor_spellings(self):
        self.assertEqual(collector.status_for("Rumoured snapshot", "", False), "Rumor")
        self.assertEqual(collector.status_for("Rumored snapshot", "", False), "Rumor")


class SourceAndParsingTests(unittest.TestCase):
    def test_official_domain_matches_subdomain(self):
        project = {"official_domains": ["example.org"]}
        self.assertTrue(collector.host_is_official("https://blog.example.org/post", project))

    def test_lookalike_domain_is_not_official(self):
        project = {"official_domains": ["example.org"]}
        self.assertFalse(collector.host_is_official("https://example.org.attacker.test/post", project))

    def test_html_is_cleaned_and_entities_decoded(self):
        self.assertEqual(collector.plain_text("<b>Token</b> &amp; points"), "Token & points")

    def test_rss_item_parsing(self):
        feed = b"""<?xml version="1.0"?><rss version="2.0"><channel><item><title>Snapshot live</title><link>https://example.org/snapshot</link><pubDate>Mon, 26 Oct 2026 12:00:00 GMT</pubDate><description>Check eligibility</description></item></channel></rss>"""
        items = collector.parse_feed(feed)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "Snapshot live")
        self.assertEqual(items[0]["url"], "https://example.org/snapshot")
        self.assertEqual(items[0]["published_at"], "2026-10-26T12:00:00Z")

    def test_invalid_xml_returns_empty_list(self):
        self.assertEqual(collector.parse_feed(b"<rss><broken>"), [])

    def test_date_normalizes_to_utc(self):
        self.assertEqual(collector.normalize_date("2026-10-26T15:00:00+03:00"), "2026-10-26T12:00:00Z")


if __name__ == "__main__":
    unittest.main()
