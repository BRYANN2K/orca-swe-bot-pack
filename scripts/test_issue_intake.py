"""Test identity and state handling across issue trackers."""

import unittest

from build import ROOT
from issue_intake import reconcile
from pack import load_json


class IssueIntakeChecks(unittest.TestCase):
    def setUp(self):
        self.snapshot = load_json(ROOT / "profiles" / "issue-intake.example.json")

    def test_open_mirrors_are_one_item_and_same_title_stays_distinct(self):
        result = reconcile(self.snapshot)
        self.assertTrue(result["coverage_complete"])
        self.assertEqual(len(result["work_items"]), 2)
        mirror = next(item for item in result["work_items"] if item["id"].startswith("work:"))
        self.assertEqual(len(mirror["issues"]), 2)
        self.assertEqual(mirror["state"], "open")
        self.assertTrue(mirror["primary"].startswith("linear:"))
        self.assertTrue(result["work_items"][0]["id"].startswith("gitlab:"))

    def test_replayed_and_reordered_snapshot_has_same_items(self):
        first = reconcile(self.snapshot)
        self.snapshot["issues"].reverse()
        self.snapshot["work_links"][0]["refs"].reverse()
        self.assertEqual(first, reconcile(self.snapshot))

    def test_new_mirror_keeps_existing_work_identity(self):
        link = self.snapshot["work_links"][0]
        link["id"] = link["refs"][0]
        result = reconcile(self.snapshot)
        work = next(item for item in result["work_items"] if item["id"] == link["id"])
        self.assertEqual(work["primary"], link["primary"])
        self.assertEqual(len(work["issues"]), 2)

    def test_missing_and_closed_mirrors_do_not_imply_done(self):
        self.snapshot["issues"][0]["status"] = "closed"
        self.assertEqual(reconcile(self.snapshot)["work_items"][1]["state"], "open")
        self.snapshot["sources"][2]["status"] = "unavailable"
        del self.snapshot["issues"][1]
        result = reconcile(self.snapshot)
        self.assertFalse(result["coverage_complete"])
        self.assertEqual(result["work_items"][1]["state"], "unknown")
        self.assertEqual(result["work_items"][1]["issues"][1]["status"], "not-observed")

    def test_conflicting_links_fail_instead_of_forking_work(self):
        link = self.snapshot["work_links"][0]
        self.snapshot["work_links"].append({**link, "id": "work:conflict"})
        with self.assertRaisesRegex(ValueError, "more than one work link"):
            reconcile(self.snapshot)


if __name__ == "__main__":
    unittest.main()
