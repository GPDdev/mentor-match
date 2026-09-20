from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "mentor_match.py"


class MentorMatchCliTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "data"
        self.work = Path(self.temp.name) / "work"
        self.work.mkdir()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_cli(self, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        command = [sys.executable, str(SCRIPT), "--root", str(self.root), *args]
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        self.assertEqual(expected, result.returncode, msg=f"stdout={result.stdout}\nstderr={result.stderr}")
        return result

    def write_artifacts(self, culture_weight: int = 5) -> tuple[Path, Path, Path, Path]:
        report = self.work / "report.md"
        csv = self.work / "candidates.csv"
        data = self.work / "candidates.json"
        log = self.work / "search-log.md"
        report.write_text("# Report\n", encoding="utf-8")
        csv.write_text("rank,candidate_id,name\n1,ada-lovelace,Ada Lovelace\n", encoding="utf-8")
        log.write_text("# Search log\n", encoding="utf-8")
        weights = {
            "research_fit": 30,
            "method_fit": 15,
            "eligibility": 15,
            "opening": 10,
            "funding": 10,
            "trajectory": 10,
            "constraints": 5,
            "advising_and_culture": culture_weight,
        }
        weights["constraints"] += 5 - culture_weight
        payload = {
            "schema_version": 1,
            "generated_at": "2026-09-19T00:00:00Z",
            "profile_id": "sample-applicant",
            "case_id": "phd-2027",
            "mode": "standard",
            "language": "en",
            "scope": {"institutions": ["Example University"]},
            "weights": weights,
            "candidates": [
                {
                    "candidate_id": "ada-lovelace",
                    "name": "Ada Lovelace",
                    "group": "Analytical Engines Lab",
                    "organization": "Example University",
                    "unit": "School of Computing",
                    "country": "Example",
                    "institution_type": "university",
                    "applicable_routes": ["phd"],
                    "score": 88.5,
                    "confidence": "high",
                    "status": "program-route",
                    "dimension_scores": {},
                    "primary_fit": "Methods align",
                    "primary_risk": "Admissions are committee-based",
                    "facts": [],
                    "inferences": [],
                    "culture_signals": [],
                    "sources": [
                        {
                            "url": "https://example.edu/ada",
                            "title": "Ada Lovelace",
                            "source_type": "official",
                            "accessed_at": "2026-09-19",
                            "supports": ["affiliation"],
                        }
                    ],
                }
            ],
        }
        data.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return report, csv, data, log

    def test_full_storage_flow(self) -> None:
        self.run_cli("init", expected=2)
        self.run_cli("init", "--accept-storage")
        resume = self.work / "resume.txt"
        resume.write_text("Synthetic resume", encoding="utf-8")
        preferences = self.work / "preferences.json"
        preferences.write_text('{"target": "phd"}', encoding="utf-8")
        self.run_cli(
            "create-profile",
            "--profile",
            "sample-applicant",
            "--display-name",
            "Sample Applicant",
            "--resume",
            str(resume),
            "--preferences",
            str(preferences),
        )
        intent = self.work / "intent.json"
        intent.write_text('{"cycle": "2027"}', encoding="utf-8")
        self.run_cli(
            "create-case",
            "--profile",
            "sample-applicant",
            "--case",
            "phd-2027",
            "--title",
            "2027 PhD search",
            "--intent",
            str(intent),
        )
        report, csv, data, log = self.write_artifacts()
        self.run_cli("validate", str(data))
        snapshot = self.run_cli(
            "snapshot",
            "--profile",
            "sample-applicant",
            "--case",
            "phd-2027",
            "--mode",
            "standard",
            "--report",
            str(report),
            "--candidates-csv",
            str(csv),
            "--candidates-json",
            str(data),
            "--search-log",
            str(log),
        )
        run_path = Path(snapshot.stdout.strip())
        self.assertTrue((run_path / "run.json").is_file())
        listing = json.loads(self.run_cli("list").stdout)
        self.assertEqual("phd-2027", listing[0]["cases"][0]["case_id"])
        exported = Path(self.run_cli("export", "--profile", "sample-applicant", "--case", "phd-2027").stdout.strip())
        self.assertTrue(exported.is_file())

    def test_rejects_excessive_culture_weight(self) -> None:
        _, _, data, _ = self.write_artifacts(culture_weight=11)
        result = self.run_cli("validate", str(data), expected=1)
        self.assertIn("culture weight may not exceed 10", result.stderr)

    def test_delete_requires_exact_confirmation(self) -> None:
        self.run_cli("init", "--accept-storage")
        self.run_cli(
            "create-profile",
            "--profile",
            "sample-applicant",
            "--display-name",
            "Sample Applicant",
        )
        self.run_cli("delete", "--profile", "sample-applicant", "--confirm", "wrong", expected=1)
        self.assertTrue((self.root / "profiles" / "sample-applicant").exists())

    def test_failed_snapshot_leaves_no_partial_run(self) -> None:
        self.run_cli("init", "--accept-storage")
        self.run_cli(
            "create-profile",
            "--profile",
            "sample-applicant",
            "--display-name",
            "Sample Applicant",
        )
        self.run_cli(
            "create-case",
            "--profile",
            "sample-applicant",
            "--case",
            "phd-2027",
            "--title",
            "2027 PhD search",
        )
        report, csv, data, log = self.write_artifacts()
        self.run_cli(
            "snapshot",
            "--profile",
            "sample-applicant",
            "--case",
            "phd-2027",
            "--mode",
            "standard",
            "--report",
            str(report),
            "--candidates-csv",
            str(csv),
            "--candidates-json",
            str(data),
            "--search-log",
            str(log),
            "--application-dir",
            str(self.work / "missing-application"),
            expected=1,
        )
        runs = self.root / "profiles" / "sample-applicant" / "cases" / "phd-2027" / "runs"
        self.assertEqual([], list(runs.iterdir()))


if __name__ == "__main__":
    unittest.main()
