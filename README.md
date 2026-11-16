# Access Review Ledger

An offline identity governance lab for reconstructing who held a permission at a given time. All event records are synthetic. The starter provides a working event inventory and regression suite. The assignment is to implement historical access reconciliation, persistent imports and reproducible audit reports.

## Quick start
```sh
python ledger.py inventory examples/grant-only/day-01.json
python -m unittest discover -s tests -v
python acceptance.py --inventory
```

Use Python 3.10 or later. No packages, network, keys or live identity provider are required. [Assignment and CLI contract](ASSIGNMENT.md) · [Reviewer brief and session worksheet](REVIEW.md). The acceptance cases target the reconciliation feature you will implement.
