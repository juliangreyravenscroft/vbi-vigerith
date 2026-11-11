
import json

max_event_bytes = 16 * 1024


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}

    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")

        result[key] = value

    return result


def _reject_nonfinite(value: str) -> None:
    raise ValueError(f"Non-JSON numeric constant: {value}")


def parse_event_json(raw: str) -> dict[str, object]:
    if not isinstance(raw, str):
        raise TypeError("Expected JSON text")

    try:
        size = len(raw.encode("utf-8"))
    except UnicodeEncodeError as exc:
        raise ValueError("Invalid Unicode input") from exc

    if size > max_event_bytes :
        raise ValueError("JSON input exceeds size limit")

    event = json.loads(
        raw,
        object_pairs_hook=_unique_object,
        parse_constant=_reject_nonfinite,
    )

    if not isinstance(event, dict):
        raise ValueError("Event must be a Json object")

    return event
