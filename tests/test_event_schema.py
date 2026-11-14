
import unittest
from pathlib import Path

from src.event_json import parse_event_json
from src.event_schema import validate_event_schema

FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "examples"
    / "security-event.v0.2.json"
)


class EventSchemaTests(unittest.TestCase):
    def setUp(self):
        self.event = parse_event_json(
            FIXTURE.read_text(encoding="utf-8")
        )

    def test_valid_example(self):
        self.assertIsNone(validate_event_schema(self.event))

    def test_missing_field(self):
        del self.event["event_name"]
        with self.assertRaisesRegex(ValueError, "missing field"):
            validate_event_schema(self.event)

    def test_extra_field(self):
        self.event["unexpected"] = True
        with self.assertRaisesRegex(ValueError, "unexpected field"):
            validate_event_schema(self.event)

    def test_wrong_type(self):
        self.event["evidence_refs"] = "abc"
        with self.assertRaisesRegex(ValueError, "expected array"):
            validate_event_schema(self.event)

    def test_wrong_version(self):
        self.event["schema_version"] = "0.3.0"
        with self.assertRaisesRegex(ValueError, "unexpected constant"):
            validate_event_schema(self.event)

    def test_unsupported_severity(self):
        self.event["severity"] = "critical"
        with self.assertRaisesRegex(ValueError, "unsupported value"):
            validate_event_schema(self.event)

    def test_blank_event_name(self):
        self.event["event_name"] = "   "
        with self.assertRaisesRegex(ValueError, "pattern mismatch"):
            validate_event_schema(self.event)

    def test_description_too_long(self):
        self.event["event_description"] = "x" * 1025
        with self.assertRaisesRegex(ValueError, "string too long"):
            validate_event_schema(self.event)

    def test_invalid_timestamp(self):
        self.event["observed_at"] = "2026-02-30T12:00:00Z"
        with self.assertRaisesRegex(ValueError, "invalid date-time"):
            validate_event_schema(self.event)

    def test_duplicate_reference(self):
        self.event["evidence_refs"] = ["evidence-1", "evidence-1"]
        with self.assertRaisesRegex(ValueError, "duplicate array item"):
            validate_event_schema(self.event)

    def test_invalid_reference_type(self):
        self.event["evidence_refs"] = [3]
        with self.assertRaisesRegex(ValueError, "expected string"):
            validate_event_schema(self.event)

    def test_empty_references_allowed(self):
        self.event["evidence_refs"] = []
        self.assertIsNone(validate_event_schema(self.event))

    def test_non_object(self):
        with self.assertRaisesRegex(ValueError, "expected object"):
            validate_event_schema([])
