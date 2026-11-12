
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

    def test_infinity_is_rejected(self):
        for value in ("Infinity", "-Infinity"):
            with self.subTest(value=value):
                raw = '{"score": ' + value + '}'
                with self.assertRaisesRegex(
                    ValueError, "Non-JSON numeric constant"
                ):
                    parse_event_json(raw)

    def test_unicode_escaped_duplicate_key(self):
        raw = '{"event_id": "first", "\\u0065vent_id": "second"}'
        with self.assertRaisesRegex(ValueError, "Duplicate JSON key"):
            parse_event_json(raw)


    def test_size_limit_boundary(self):
        prefix = '{"data":"'
        suffix = '"}'
        padding_size = max_event_bytes - len(prefix.encode("utf-8")) - len(
            suffix.encode("utf-8")
        )
        raw = prefix + ("x" * padding_size) + suffix

        # Exactly at the limit: accepted.
        self.assertEqual(len(raw.encode("utf-8")), max_event_bytes)
        self.assertIsInstance(parse_event_json(raw), dict)

        # One byte over the limit: rejected.
        oversized = raw[:-2] + "x" + suffix

        self.assertEqual(
            len(oversized.encode("utf-8")), max_event_bytes + 1
        )

        with self.assertRaisesRegex(ValueError, "size limit"):
            parse_event_json(oversized)
