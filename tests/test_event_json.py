
import unittest
from pathlib import Path

from src.event_json import max_event_bytes, parse_event_json

FIXTURE = Path(__file__).resolve().parents[1] / "examples" / "security-event.v0.2.json"


class EventJsonTests(unittest.TestCase):
    def test_example_is_parsed(self):
        raw = FIXTURE.read_text(encoding="utf-8")
        event = parse_event_json(raw)
        self.assertEqual(event["event_id"], "evt-0001")

    def test_duplicate_top_level_key(self):
        raw = '{"event_id": "first", "event_id": "second"}'
        with self.assertRaisesRegex(ValueError, "Duplicate JSON key"):
            parse_event_json(raw)

    def test_duplicate_nested_key(self):
        raw = '{"details": {"result": "a", "result": "b"}}'
        with self.assertRaisesRegex(ValueError, "Duplicate JSON key"):
            parse_event_json(raw)

    def test_non_json_number(self):
        with self.assertRaisesRegex(ValueError, "Non-JSON numeric constant"):
            parse_event_json('{"score": NaN}')

    def test_non_object_root(self):
        with self.assertRaisesRegex(ValueError, "Event must be a Json object"):
            parse_event_json("[]")

    def test_size_limit(self):
        raw = '{"data":"' + "x" * max_event_bytes + '"}'
        with self.assertRaisesRegex(ValueError, "size limit"):
            parse_event_json(raw)

    def test_malformed_json(self):
        with self.assertRaises(ValueError):
            parse_event_json('{"event_id":')

    def test_wrong_input_type(self):
        with self.assertRaises(TypeError):
            parse_event_json(123)
