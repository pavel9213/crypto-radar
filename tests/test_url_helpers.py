"""Tests for URL helper behavior in the news collector."""
import importlib.util
import pathlib
import unittest
from urllib.parse import parse_qs, urlparse

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("collect_news", ROOT / "scripts" / "collect_news.py")
collector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(collector)


class URLHelperTests(unittest.TestCase):
    def test_google_news_query_is_encoded_and_parseable(self):
        url = collector.google_news_url('"sample chain"')
        parsed = urlparse(url)
        self.assertEqual(parsed.scheme, "https")
        self.assertEqual(parsed.netloc, "news.google.com")
        self.assertEqual(parse_qs(parsed.query)["q"], ['"sample chain"'])

    def test_official_host_is_case_insensitive(self):
        project = {"official_domains": ["example.org"]}
        self.assertTrue(collector.host_is_official("https://BLOG.Example.org/post", project))

    def test_unrelated_host_is_not_official(self):
        project = {"official_domains": ["example.org"]}
        self.assertFalse(collector.host_is_official("https://example.net/post", project))


if __name__ == "__main__":
    unittest.main()
