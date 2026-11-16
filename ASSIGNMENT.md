# Historical access reconciliation

Implement three commands in the existing CLI using the Python standard library:

```
python ledger.py import --db review.sqlite examples/grant-only/day-01.json
python ledger.py report --db review.sqlite --tenant ember --at 2026-01-01T00:00:00Z --format json
python ledger.py report --db review.sqlite --tenant ember --at 2026-01-01T00:00:00Z --format csv
```

Import reads only the events array from a JSON object. Ignore fixture metadata. Validate field types, nonempty identifiers, supported kinds, timezone-aware ISO timestamps and optional grant expires_at strictly later than at. Normalize timestamps to UTC. Identity is (tenant, event id). Reimporting an identical normalized event is a no-op. A conflicting duplicate or malformed row rejects the entire batch and preserves earlier imports. Use a SQLite transaction and a unique constraint so concurrent imports cannot duplicate rows.

Replay per (tenant, subject, role), including events at the cutoff. Sort by instant then event id in ascending Unicode code point order. Grant replaces earlier state with pending and an optional expiration. Approve changes pending to active and retains its expiry. Deny changes pending to denied. Revoke changes pending or active to revoked. Other transitions are ignored. If an expiry instant is reached, pending or active becomes expired before processing events at that instant. A fresh grant resets expiry. Terminal states persist until a fresh grant. Omit keys without an effective grant. Scope every query to the requested tenant; an unknown tenant has an empty report.

JSON is an array of objects with exactly subject, role and status, sorted by subject then role. CSV uses those columns in that order and includes the header for empty output. Use standard CSV quoting. Emit reports on stdout and validation diagnostics on stderr, return nonzero on invalid requests, and keep report read-only. Preserve the existing inventory command.

## Estimated hands-on work
| Work | Minutes |
| --- | ---: |
| Trace the baseline, model events and document replay invariants | 45 |
| Build transactional SQLite import, validation and conflict handling | 80 |
| Implement historical replay, expiration and deterministic ties | 85 |
| Integrate CLI, JSON and CSV reporting | 50 |
| Test isolation, retries, rollback, simultaneous imports and boundary times | 75 |
| Run acceptance, record evidence and update usage notes | 25 |

Total estimate: 360 minutes. Record actual time worked.
