
def validate_event(event: object) -> bool:
    if not isinstance(event, dict):
        return False

    required_fields = ("event_id", "source", "severity")

    for field in required_fields:
        value = event.get(field)

        if not isinstance(value, str):
            return False

        if not value.strip():
            return False

    return event["severity"] in ("low", "medium", "high")
