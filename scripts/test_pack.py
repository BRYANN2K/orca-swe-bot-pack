"""Local checks for the conditions that should stop a bot setup or handoff."""

import json
import tempfile
import unittest
from pathlib import Path

from build import ROOT, valid_cron
from pack import load_json, plan_routines, validate_handoff, validate_profile


def confirmed_profile(name="stipulate"):
    profile = load_json(ROOT / "profiles" / f"{name}.json")
    profile.update(repository="pilot/widget", host="pilot-01", timezone="Europe/Brussels")
    profile["spec"]["approval_signal"] = "Owner-approved revision in the tracked change"
    profile["ci"]["provider"] = "Manual verification"
    return profile


class PackChecks(unittest.TestCase):
    def test_three_workflows_use_the_same_contract(self):
        for workflow in ("stipulate", "openspec", "markdown-main"):
            with self.subTest(workflow=workflow):
                validate_profile(confirmed_profile(workflow))
                with self.assertRaisesRegex(ValueError, "real repository"):
                    validate_profile(load_json(ROOT / "profiles" / f"{workflow}.json"))

    def test_profile_rejects_missing_approval_and_invalid_timezone(self):
        profile = confirmed_profile()
        profile["spec"]["approval_signal"] = None
        with self.assertRaisesRegex(ValueError, "approval_signal"):
            validate_profile(profile)
        profile = confirmed_profile()
        profile["timezone"] = "Mars/Test"
        with self.assertRaisesRegex(ValueError, "IANA timezone"):
            validate_profile(profile)

    def test_json_rejects_duplicate_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profile.json"
            path.write_text('{"host":"first","host":"second"}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Duplicate JSON key"):
                load_json(path)

    def test_plan_is_stable_paused_and_private(self):
        profile = confirmed_profile()
        args = (profile, "pr-review-docs", "Review", ["review-catchup"], [])
        plan = plan_routines(*args)
        self.assertEqual(plan, plan_routines(*args))
        routine = plan["routines"][0]
        argv = routine["argv"]
        self.assertIn("--disabled", argv)
        self.assertEqual(argv[argv.index("--results-to") + 1], "chat")
        self.assertEqual(argv[argv.index("--timezone") + 1], "Europe/Brussels")
        existing = plan_routines(*args, existing_names=[routine["name"]])
        self.assertEqual(existing["routines"][0]["status"], "review-existing")
        self.assertNotIn("argv", existing["routines"][0])

    def test_event_needs_confirmed_capability_and_repo_scope(self):
        profile = confirmed_profile()
        args = (profile, "repo-maintenance", "Repo maintenance", ["merge-closure"])
        with self.assertRaisesRegex(ValueError, "trigger options"):
            plan_routines(*args, [])
        argv = plan_routines(*args, ["github.pr_merged"])["routines"][0]["argv"]
        self.assertIn("github.pr_merged in=pilot/widget", argv)
        self.assertIn("--disabled", argv)

    def test_changed_head_or_contract_invalidates_handoff(self):
        handoff = load_json(ROOT / "profiles" / "handoff.example.json")
        profile = confirmed_profile()
        handoff["repository"] = profile["repository"]
        head = handoff["candidate"]["head_sha"]
        contract = handoff["contract"]["ref"]
        self.assertFalse(validate_handoff(handoff, profile, head, contract))
        handoff["criteria"][0].update(status="passed", evidence=json.dumps({"run": "CI-42"}))
        self.assertTrue(validate_handoff(handoff, profile, head, contract))
        with self.assertRaisesRegex(ValueError, "candidate head changed"):
            validate_handoff(handoff, profile, "f" * 40, contract)
        with self.assertRaisesRegex(ValueError, "approved contract changed"):
            validate_handoff(handoff, profile, head, "different")

    def test_cron_rejects_out_of_range_and_reversed_fields(self):
        self.assertTrue(valid_cron("40 9 * * 1-5"))
        for expression in ("60 9 * * 1-5", "0 24 * * *", "0 9 0 * *", "0 9 * * 5-1"):
            with self.subTest(cron=expression):
                self.assertFalse(valid_cron(expression))


if __name__ == "__main__":
    unittest.main()
