# VIGERITH

**Cross-Domain Security Intelligence and Systems Assurance**

**RAVENSCROFT INDUSTRIES**
*RAVENSCROFT Engineering Program*

> Evidence before conclusions. Verification before release.

## Brand and Product Structure

**RAVENSCROFT INDUSTRIES** is the primary identity for this engineering and research portfolio. **VanceBlackwood** is a planned product initiative under RAVENSCROFT INDUSTRIES, not a separate parent organization. **VIGERITH** is the security intelligence and systems assurance research component within this portfolio, with work that may inform the VanceBlackwood product direction.

This describes an intended project structure. The repository does not claim legal incorporation, an available commercial service, or a released product.

## Mission

VIGERITH is a security engineering research project focused on reliable telemetry, evidence-based analysis, and the assurance of interconnected software and hardware systems.

The objective is to turn fragmented observations into structured findings that can be inspected, reproduced, and challenged. Parsing, validation, provenance, detection, and reporting have distinct responsibilities. A structurally valid record does not prove that an event occurred. A detection hypothesis is not a verified finding.

Development begins with a small, testable event ingestion foundation. Additional capabilities will be introduced only when their contracts, trust boundaries, and failure conditions can be explained and verified.

## Implementation Status

The `feature/event-schema-v0.2` branch contains an early security event validation prototype using synthetic data. The work remains experimental and has not been released.

| Component | Responsibility | State |
| --- | --- | --- |
| Baseline event validator | Checks a minimal set of required event fields and severity values | Implemented prototype |
| Strict JSON parser | Rejects malformed input, duplicate object keys, nonstandard numeric constants, and oversized JSON text | Implemented prototype |
| Security event schema v0.2 | Defines the current event structure and field constraints using JSON Schema Draft 2020-12 | Defined contract |
| Schema validation module | Evaluates the subset of schema rules required by the current contract | Implemented prototype |
| Synthetic event example | Provides a reproducible input for parsing and validation tests | Available |
| Unit tests | Exercise parser rejection paths, schema constraints, time zone handling, evidence references, and length boundaries | Implemented on this branch, CI verification pending |

The parser enforces a 16 KiB limit on UTF-8 input, requires a JSON object at the root, and rejects duplicate keys after JSON escape decoding. The input limit is a prototype policy, not a measured production capacity.

The schema validator implements the subset of rules used by the current contract, not the complete JSON Schema specification. Date-time validation follows a project-specific policy and does not establish full RFC 3339 compliance. Unsupported keywords are checked only in rules reached during event validation. There is no separate schema compilation or full schema-definition validation step. Comparison with a reference implementation remains open work.

No operational ingestion service, correlation engine, detection platform, or public release is available.

## Security Event Contract

The v0.2 contract currently defines these fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Identifies the expected event contract version |
| `event_id` | Carries the proposed identifier for a single event record; uniqueness is not yet enforced |
| `event_name` | Provides a readable event label |
| `event_type` | Holds the declared event type |
| `event_description` | Provides descriptive context, limited to 1024 characters |
| `source` | Records the source identifier reported in the event |
| `severity` | Restricts the declared severity to low, medium, or high |
| `observed_at` | Records the reported observation time |
| `evidence_refs` | Holds distinct nonblank evidence reference strings |

The validator checks structure, not truth. It does not enforce global uniqueness of `event_id`, authenticate `source`, verify that evidence references exist, or substantiate claims in `event_description`. Event classes, authoritative identifiers, and correlation rules have not yet been established.

Future event modeling will distinguish an individual record from its classification and from relationships inferred across multiple records. Related observations must remain independently traceable.

## Processing Boundaries

The implemented prototype covers parsing and structural validation. The broader pipeline remains a research target.

```text
Synthetic event JSON
        |
Strict JSON parsing
        |
Python event object
        |
Schema validation
        |
Structurally accepted event
        |
Provenance and identity checks     Planned
        |
Detection and correlation          Planned
        |
Human review and reporting         Planned
```

Structural acceptance does not establish source authenticity, authorization, evidence integrity, or incident severity.

## Repository Guide

| Path | Purpose |
| --- | --- |
| `src/validate_event.py` | Initial minimal event validation experiment |
| `src/event_json.py` | Strict JSON parsing boundary |
| `src/event_schema.py` | Current schema validation logic |
| `schemas/security-event.v0.2.schema.json` | Versioned event contract |
| `examples/security-event.v0.2.json` | Synthetic event fixture |
| `tests/test_validate_event.py` | Tests for the baseline validator |
| `tests/test_event_json.py` | Parser behavior and security boundary tests |
| `tests/test_event_schema.py` | Schema rules and boundary tests |
| `.github/workflows/python-tests.yml` | Automated unit test workflow |

The dependencies are directional. `src/event_json.py` parses untrusted JSON text and has no dependency on the schema validator. `src/event_schema.py` imports `parse_event_json()` to load the versioned schema, then checks event dictionaries against the supported rules. `tests/test_event_json.py` exercises the parser independently. `tests/test_event_schema.py` loads the synthetic fixture through the parser and checks schema behavior. The baseline validator in `src/validate_event.py` remains separate. These files are not yet integrated into an ingestion service.

## Verification

From the repository root on the development branch, check the JSON files and run the complete unit test suite:

```bash
python3 -m json.tool examples/security-event.v0.2.json > /dev/null
python3 -m json.tool schemas/security-event.v0.2.schema.json > /dev/null
python3 -m unittest discover -s tests -v
```

The test suite covers selected accepted and rejected length boundaries, time zone handling, and whitespace-only evidence references. Passing these tests supports specific behavior claims, not exhaustive correctness.

GitHub Actions runs on pushes to `main` and pull requests targeting `main`. A passing run on `main` does not verify unmerged changes on this branch. Before merging, the proposed commit needs passing CI checks, review of failure cases, and an explicit record of known limitations.

## Engineering Principles

- Preserve individual event records and their identifiers when investigating related activity.
- Separate observed data, inferred relationships, and verified conclusions.
- Treat external event content as untrusted until the relevant controls have been applied.
- Prefer explicit contracts, narrow interfaces, and failures that can be diagnosed.
- Test valid boundaries as carefully as invalid inputs.
- Avoid features that add complexity without a defined problem or measurable benefit.
- Record what has been verified and what remains an assumption.

## Engineering Review

Changes begin with a defined problem, a technical rationale, and explicit acceptance criteria. Development proceeds through a design review, implementation, a line-by-line walkthrough of affected files and interfaces, targeted verification, an independent extension exercise, and final review. Tests must cover expected behavior, rejection paths, and relevant boundaries. A passing test is evidence for the case it exercises, not a general proof of correctness. Unexplained or nonreproducible changes are not ready for approval.

## Research Domains

| Domain | Research direction |
| --- | --- |
| Security telemetry and detection | Event modeling, ingestion, correlation, detection quality, and false-positive analysis |
| Malware intelligence and reverse engineering | Controlled analysis, behavioral evidence, and defensive indicators |
| Threat intelligence and digital forensics | Provenance, source evaluation, incident records, and reproducible findings |
| Firmware and embedded security | Firmware integrity, secure updates, boot-chain assurance, and attack-surface research |
| FPGA and trusted hardware assurance | RTL security properties, programmable logic, and hardware-software trust boundaries |
| UAS and cyber-physical security | Unarmed simulation, read-only telemetry, system assurance, and resilience |
| AI-assisted security analysis | Explainable assistance, validation controls, and measurable analytical performance |

These are areas for future research. They are not implemented capabilities of the current prototype.

## Development Roadmap

1. **Contract hardening:** Validate schema definitions before processing events, strengthen boundary tests, and compare results with a reference implementation.
2. **Event identity and provenance:** Define source event identifiers, duplicate-delivery handling, evidence references, and trustworthy origin records.
3. **Correlation research:** Link related records without merging their identities, with explicit time-window and uncertainty rules.
4. **Detection evaluation:** Measure incorrect classifications, coverage, performance, and reproducibility using controlled datasets.
5. **Cross-domain assurance:** Extend validated interfaces to isolated firmware, embedded, hardware, and simulated cyber-physical research.

Progress is measured through reviewed code, reproducible tests, and documented engineering decisions rather than feature counts.

## Research Boundaries

Testing is restricted to owned, explicitly authorized, or isolated laboratory environments. Malware research remains contained. Work involving UAS and defense systems begins with unarmed simulation, read-only telemetry, and assurance testing. Live control and weapon-related capabilities are outside the present scope.

Credentials, sensitive personal data, restricted material, and unreviewed research artifacts must not be committed to this repository.

## Program Context

VIGERITH is a research component of RAVENSCROFT INDUSTRIES under the RAVENSCROFT Engineering Program. It complements SILIARCH, which focuses on trusted hardware and embedded engineering. Any future integration with other research components or the VanceBlackwood product initiative requires explicit interfaces, testable contracts, and clearly assigned security responsibilities.

**RAVENSCROFT INDUSTRIES**

*RAVENSCROFT Engineering Program | VIGERITH Security Research*

**Understand the system. Define the boundary. Verify the result.**
