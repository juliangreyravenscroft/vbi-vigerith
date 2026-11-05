
import unittest

from src.validate_event import validate_event


class EventValidatorTests(unittest.TestCase):
    def test_valid_event(self):
        event = {"event_id": "evt-001", "source": "lab-host-01", "severity": "high"}
        self.assertTrue(validate_event(event))

    def test_missing_field(self):
        event = {"event_id": "evt-001", "severity": "low"}
        self.assertFalse(validate_event(event))

    def test_blank_value(self):
        event = {"event_id": " ", "source": "lab-host-01", "severity": "low"}
        self.assertFalse(validate_event(event))

    def test_invalid_severity(self):
        event = {"event_id": "evt-001", "source": "lab-host-01", "severity": "critical"}
        self.assertFalse(validate_event(event))

    def test_wrong_input_type(self):
        self.assertFalse(validate_event(["not", "a", "dictionary"]))

