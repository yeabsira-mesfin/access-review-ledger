"""Offline inventory for synthetic access review events."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

KINDS = {"grant", "approve", "revoke", "deny"}


def read_events(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    events = data["events"]
    if not isinstance(events, list):
        raise ValueError("events must be a list")
    for event in events:
        for field in ("id", "tenant", "subject", "role", "at", "kind"):
            if not isinstance(event.get(field), str) or not event[field].strip():
                raise ValueError(f"invalid {field}")
        if event["kind"] not in KINDS:
            raise ValueError("unknown event kind")
    return events


def inventory(events):
    return {"events": len(events), "by_kind": dict(Counter(e["kind"] for e in events)),
            "tenants": sorted({e["tenant"] for e in events})}


def main():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("inventory").add_argument("file", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(inventory(read_events(args.file)), sort_keys=True))
    except (KeyError, ValueError, OSError, AttributeError, TypeError) as exc:
        print(f"Invalid event input: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
