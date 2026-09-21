from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "verify_expansion_contract.py"

spec = importlib.util.spec_from_file_location("verify_expansion_contract", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class ExpansionContractTest(unittest.TestCase):
    def test_contract_is_valid(self) -> None:
        self.assertEqual(module.validate(), [])


if __name__ == "__main__":
    unittest.main()
