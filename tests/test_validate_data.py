"""Tests for the JSON validation helpers."""
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_data", ROOT / "scripts" / "validate_data.py")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def good_config():
    return {
        "projects": [{
            "id": "sample", "name": "Sample", "keywords": ["sample chain"],
            "official_urls": ["https://example.org/"], "official_domains": ["example.org"],
            "x_handles": ["sample"]
        }],
        "poll_interval_hours": 4, "max_events": 250
    }


def good_event():
    return {
        "id": "event-1", "projectId": "sample", "project": "Sample", "category": "TGE",
        "title": "Official token launch", "status": "Confirmed", "date": "2026-10-26",
        "publishedAt": "2026-10-26T12:00:00Z", "source": "https://example.org/news",
        "sourceName": "example.org", "sourceType": "official", "automatic": True, "notes": "Test"
    }


class ConfigValidationTests(unittest.TestCase):
    def test_valid_config_passes(self):
        self.assertEqual(validator.validate_config(good_config()), [])

    def test_duplicate_project_ids_are_rejected(self):
        config = good_config()
        config["projects"].append(dict(config["projects"][0]))
        self.assertTrue(any("duplicate project id" in e for e in validator.validate_config(config)))

    def test_invalid_website_scheme_is_rejected(self):
        config = good_config()
        config["projects"][0]["official_urls"] = ["javascript:alert(1)"]
        self.assertTrue(any("HTTP(S) URL" in e for e in validator.validate_config(config)))

    def test_invalid_handle_is_rejected(self):
        config = good_config()
        config["projects"][0]["x_handles"] = ["this-handle-is-too-long"]
        self.assertTrue(any("invalid X handle" in e for e in validator.validate_config(config)))


class FeedValidationTests(unittest.TestCase):
    def test_valid_feed_event_passes(self):
        self.assertEqual(validator.validate_feed({"events": [good_event()]}), [])

    def test_duplicate_event_ids_are_rejected(self):
        event = good_event()
        self.assertTrue(any("duplicate event id" in e for e in validator.validate_feed({"events": [event, dict(event)]})))

    def test_non_http_source_is_rejected(self):
        event = good_event()
        event["source"] = "file:///etc/passwd"
        self.assertTrue(any("HTTP(S) URL" in e for e in validator.validate_feed({"events": [event]})))

    def test_invalid_status_and_date_are_rejected(self):
        event = good_event()
        event["status"] = "Probably true"
        event["date"] = "yesterday"
        errors = validator.validate_feed({"events": [event]})
        self.assertTrue(any(".status:" in e for e in errors))
        self.assertTrue(any(".date:" in e for e in errors))

    def test_timestamp_requires_timezone(self):
        event = good_event()
        event["publishedAt"] = "2026-10-26T12:00:00"
        self.assertTrue(any("must include a timezone" in e for e in validator.validate_feed({"events": [event]})))

    def test_missing_events_array_is_rejected(self):
        self.assertTrue(any("feed.events" in e for e in validator.validate_feed({})))


if __name__ == "__main__":
    unittest.main()
