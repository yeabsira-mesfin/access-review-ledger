import json
from pathlib import Path
import tempfile
import unittest

from ledger import inventory, read_events


class InventoryTests(unittest.TestCase):
    def test_empty_inventory(self):
        self.assertEqual(inventory([]), {"events": 0, "by_kind": {}, "tenants": []})

    def test_counts_and_order(self):
        rows = [{"kind": "grant", "tenant": "b"}, {"kind": "grant", "tenant": "a"}]
        self.assertEqual(inventory(rows), {"events": 2, "by_kind": {"grant": 2}, "tenants": ["a", "b"]})

    def test_rejects_missing_fields(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "input.json"
            path.write_text(json.dumps({"events": [{"kind": "approve"}]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "invalid id"):
                read_events(path)
