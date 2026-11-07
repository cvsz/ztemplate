from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
SCRIPTS = ROOT / "scripts"


class PrivilegedAutomationRemovalTests(unittest.TestCase):
    def test_legacy_privileged_artifacts_are_absent(self):
        forbidden_paths = (
            ".github/workflows/automated-audit-review-approve.yml",
            ".github/workflows/auto-fix-open-prs.yml",
            ".github/scripts/post-review-comment.sh",
            ".github/scripts/gpg-loopback.sh",
            "scripts/deploy-workflow-all-repos.sh",
            "scripts/auto-fix-loop.sh",
            "docs/ai/playbooks/auto-audit-review-approve-policedbc.md",
        )
        for relative_path in forbidden_paths:
            with self.subTest(path=relative_path):
                self.assertFalse((ROOT / relative_path).exists())

    def test_actions_workflows_do_not_reference_reviewer_or_gpg_secrets(self):
        for path in WORKFLOWS.rglob("*"):
            if not path.is_file() or path.suffix not in {".yml", ".yaml"}:
                continue
            source = path.read_text(encoding="utf-8")
            with self.subTest(workflow=path.relative_to(ROOT).as_posix()):
                self.assertNotIn("secrets.POLIEDBC_PAT", source)
                self.assertNotIn("secrets.GPG_SIGNING_KEY", source)
                self.assertNotIn("secrets.GPG_PASSPHRASE", source)
                self.assertNotRegex(source, re.compile(r"gh\s+pr\s+review\s+--approve"))

    def test_shell_scripts_do_not_retrieve_reviewer_or_gpg_secrets(self):
        for path in SCRIPTS.rglob("*.sh"):
            source = path.read_text(encoding="utf-8")
            with self.subTest(script=path.relative_to(ROOT).as_posix()):
                self.assertNotIn("POLIEDBC_PAT", source)
                self.assertNotIn("GPG_PASSPHRASE", source)

    def test_independent_review_workflow_is_request_only(self):
        path = WORKFLOWS / "request-independent-review.yml"
        self.assertTrue(path.is_file())
        source = path.read_text(encoding="utf-8")
        self.assertIn("pull_request_target", source)
        self.assertIn("requested_reviewers", source)
        self.assertIn("verify-independent-approval", source)
        self.assertNotIn("actions/checkout", source)
        self.assertNotIn("secrets.", source)
        self.assertNotIn("gh pr review", source)
        self.assertNotIn("gh pr merge", source)


if __name__ == "__main__":
    unittest.main()
