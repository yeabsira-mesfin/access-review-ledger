"""Black-box CLI checks using an isolated database for each example."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def run(*args):
    result = subprocess.run([sys.executable, str(ROOT / "ledger.py"), *args],
                            capture_output=True, text=True, timeout=15)
    if result.returncode:
        raise ValueError(result.stderr.strip())
    return result.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", action="store_true")
    args = parser.parse_args()
    paths = sorted((ROOT / "examples").glob("*/*.json"))
    if len(paths) != 72:
        parser.error(f"expected 72 files, found {len(paths)}")
    failed = 0
    for path in paths:
        fixture = json.loads(path.read_text(encoding="utf-8"))
        if args.inventory:
            continue
        with tempfile.TemporaryDirectory() as temp:
            db = str(Path(temp) / "review.sqlite")
            try:
                run("import", "--db", db, str(path))
                output = run("report", "--db", db, "--tenant", fixture["tenant"],
                             "--at", fixture["cutoff"], "--format", "json")
                if json.loads(output) != fixture["expected"]:
                    raise ValueError("observed report: " + output)
            except (ValueError, subprocess.TimeoutExpired) as error:
                print(f"{path.relative_to(ROOT)}: {error}", file=sys.stderr)
                failed += 1
    print(f"{len(paths)} fixtures loaded" if args.inventory else
          f"{len(paths) - failed}/{len(paths)} historical reports passed")
    return int(bool(failed))


if __name__ == "__main__":
    sys.exit(main())
