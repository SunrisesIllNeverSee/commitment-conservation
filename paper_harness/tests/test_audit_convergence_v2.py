"""Offline regression tests for the archived empirical correction."""
import json
import unittest
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from paper_harness.audit_convergence_v2 import audit_data,run


class AuditConvergenceTest(unittest.TestCase):
    def setUp(self):
        self.summary=run()

    def test_raw_sha_is_frozen(self):
        self.assertEqual(self.summary["source"]["sha256"],
                         "746aa4ec7066b1231dde7e06e7d0f2fa7bd59274c28ec1dcc5131077e8a6df19")

    def test_population_and_buckets(self):
        self.assertEqual(self.summary["signals_total"],20)
        self.assertEqual(self.summary["step"],10)
        v=self.summary["metrics"]["nli_judgment"]
        self.assertEqual(v["gate"]["n"],20)
        self.assertEqual(v["baseline"]["n"],20)
        self.assertAlmostEqual(v["gate"]["mean"],.775)
        self.assertAlmostEqual(v["baseline"]["mean"],.875)
        self.assertAlmostEqual(v["gate_minus_baseline_paired"]["mean"],-.1)
        self.assertEqual(v["gate_minus_baseline_paired"]["gate_losses"],6)
        self.assertEqual(v["gate_minus_baseline_paired"]["gate_wins"],3)
        self.assertEqual(v["gate_minus_baseline_paired"]["ties"],11)

    def test_lexical_nulls_and_n(self):
        v=self.summary["metrics"]["lexical_stability"]
        self.assertEqual(v["gate"]["n"],18)
        self.assertEqual(v["baseline"]["n"],18)
        self.assertAlmostEqual(v["gate"]["mean"],.332777778)
        self.assertAlmostEqual(v["baseline"]["mean"],.464166667)
        self.assertEqual(self.summary["coverage"]["lexical_stability"]["missing_by_regime"]["gate"],
                         ["definition","rule"])

    def test_missingness_failure_contract(self):
        source=json.loads((ROOT/"working/runs_archive/2026-03-17/convergence_v2_234059.json").read_text())
        source[0]["gate_nli"][-1]["nli_stability"]=None
        result=audit_data(source)
        self.assertEqual(result["metrics"]["nli_judgment"]["gate"]["n"],19)

    def test_fails_closed_on_duplicate_signal(self):
        source=json.loads((ROOT/"working/runs_archive/2026-03-17/convergence_v2_234059.json").read_text())
        source[1]["category"]=source[0]["category"]
        with self.assertRaises(ValueError):audit_data(source)

    def test_fails_closed_on_missing_step(self):
        source=json.loads((ROOT/"working/runs_archive/2026-03-17/convergence_v2_234059.json").read_text())
        source[0]["baseline_nli"].pop()
        with self.assertRaises(ValueError):audit_data(source)


if __name__=="__main__":
    unittest.main()
