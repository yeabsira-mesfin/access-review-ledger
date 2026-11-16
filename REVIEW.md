# Task description
I have a working offline event inventory, but it only counts access events. I need to answer who held a particular role on a historical date, even when approvals arrived late, grants expired, or an administrator revoked access. Add a SQLite importer and a tenant-scoped report to ledger.py. Preserve inventory, handle retries and partial failures, and support reproducible JSON and CSV reports. See ASSIGNMENT.md for transition semantics and command examples.

## How to judge completion
Run `python -m unittest discover -s tests -v` and `python acceptance.py` from the repository root. Expect the original tests and all 72 temporal examples to pass. Then import overlapping batches into a temporary database, replay a duplicate, introduce a conflicting duplicate at the end of a batch and verify rollback. Test two simultaneous importers, a timestamp with a non-UTC offset, equal-time events with reversed input order, an unknown tenant, and a CSV field containing a comma. Compare parsed JSON and CSV for the same tenant and cutoff. Run the inventory command on the starter sample again.

## Other notes for reviewers
All subjects and access histories are synthetic. Keep tests offline and use temporary databases. The example matrix exercises temporal decisions; the implementer should add focused tests for persistence, input validation, concurrency, multiple subjects and report formatting. Cite actual outputs and observed behavior.

## Submission worksheet
- Live compare problem ID: copy the new platform ID.
- Total hours worked: use active minutes divided by 60.
- Primary language: Python.
- Task description, completion criteria and other reviewer notes: use the three sections above.
- Task type: feature implementation with persistence and regression testing.
- Source: a new MIT-licensed, synthetic project prepared with Codex for this session.
- How the task ended: record the actual outcome.
- If completed, how checked: paste commands, test counts, exit status and one real report.
- What to inspect: ledger.py, any new storage/replay modules, tests/, acceptance.py and the updated README. Record actual changed paths.
- Turns and flags: enter observed counts. Choose only categories that occurred (writing, intent disambiguation, knowledge-state calibration, effort calibration, unstated constraints, proactivity calibration, honesty, overconfidence, agentic safety, other, or none).
- Supporting evidence: quote the exact turn and explain its effect.
