
import re
from datetime import datetime
from pathlib import Path

from src.event_json import parse_event_json

SCHEMA_PATH = (
    Path(__file__).resolve().parents[1]
    / "schemas"
    / "security-event.v0.2.schema.json"
)

SUPPORTED = {
    "$schema", "title", "description", "type", "required",
    "properties", "additionalProperties", "const", "enum",
    "minLength", "maxLength", "pattern", "format",
    "items", "uniqueItems",
}

DATE_TIME = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})\Z"
)


def _check(value: object, rule: dict, path: str) -> None:
    unknown = set(rule) - SUPPORTED
    if unknown:
        raise NotImplementedError(
            f"Unsupported schema keywords: {sorted(unknown)}"
        )

    if "type" in rule:
        kinds = {"object": dict, "array": list, "string": str}
        kind = rule["type"]

        if kind not in kinds:
            raise NotImplementedError(f"Unsupported schema type: {kind}")

        if not isinstance(value, kinds[kind]):
            raise ValueError(f"{path}: expected {kind}")

    if "const" in rule and value != rule["const"]:
        raise ValueError(f"{path}: unexpected constant")

    if "enum" in rule and value not in rule["enum"]:
        raise ValueError(f"{path}: unsupported value")

    if isinstance(value, str):
        if "minLength" in rule and len(value) < rule["minLength"]:
            raise ValueError(f"{path}: string too short")

        if "maxLength" in rule and len(value) > rule["maxLength"]:
            raise ValueError(f"{path}: string too long")

        if "pattern" in rule and re.search(rule["pattern"], value) is None:
            raise ValueError(f"{path}: pattern mismatch")

        if "format" in rule:
            if rule["format"] != "date-time":
                raise NotImplementedError(
                    f"Unsupported format: {rule['format']}"
                )

            if DATE_TIME.fullmatch(value) is None:
                raise ValueError(f"{path}: invalid date-time syntax")

            try:
                datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError as exc:
                raise ValueError(f"{path}: invalid date-time value") from exc

    if isinstance(value, dict):
        for name in rule.get("required", []):
            if name not in value:
                raise ValueError(f"{path}: missing field {name}")

        properties = rule.get("properties", {})

        if (
            "additionalProperties" in rule
            and rule["additionalProperties"] is not False
        ):
            raise NotImplementedError(
                "Only additionalProperties=false is supported"
            )

        for name, item in value.items():
            if name in properties:
                _check(item, properties[name], f"{path}.{name}")
            elif rule.get("additionalProperties") is False:
                raise ValueError(f"{path}: unexpected field {name}")

    if isinstance(value, list):
        if "items" in rule:
            for position, item in enumerate(value):
                _check(item, rule["items"], f"{path}[{position}]")

        if rule.get("uniqueItems") is True:
            for index, item in enumerate(value):
                if item in value[:index]:
                    raise ValueError(f"{path}: duplicate array item")


def validate_event_schema(event: object) -> None:
    schema = parse_event_json(
        SCHEMA_PATH.read_text(encoding="utf-8")
    )
    _check(event, schema, "$")
