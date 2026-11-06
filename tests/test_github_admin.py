"""GitHub administration helper safety tests."""

import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.github_admin import REQUIRED_CHECKS, apply, protection_payload

ROOT = Path(__file__).resolve().parents[1]


class ProtectionPayloadTest(unittest.TestCase):
    def test_new_protection_uses_baseline_without_template_repository_default(self):
        payload = protection_payload()

        self.assertEqual(payload["required_status_checks"]["contexts"], sorted(REQUIRED_CHECKS))
        self.assertTrue(payload["required_status_checks"]["strict"])
        self.assertIsNone(payload["restrictions"])
        self.assertFalse(payload["required_linear_history"])
        self.assertFalse(payload["allow_force_pushes"])
        self.assertFalse(payload["allow_deletions"])

    def test_existing_checks_and_restrictions_are_preserved(self):
        existing = {
            "required_status_checks": {
                "strict": False,
                "contexts": ["legacy-ci", "checks-ci"],
                "checks": [
                    {"context": "checks-ci", "app_id": 12},
                    {"context": "release-gate", "app_id": 99},
                ],
            },
            "required_pull_request_reviews": {
                "required_approving_review_count": 3,
                "dismiss_stale_reviews": False,
                "require_code_owner_reviews": False,
                "require_last_push_approval": False,
                "dismissal_restrictions": {
                    "users": [{"login": "reviewer"}],
                    "teams": [{"slug": "security"}],
                    "apps": [{"slug": "review-bot"}],
                },
                "bypass_pull_request_allowances": {
                    "users": [{"login": "release-manager"}],
                    "teams": [],
                    "apps": [],
                },
            },
            "restrictions": {
                "users": [{"login": "release-manager"}],
                "teams": [{"slug": "maintainers"}],
                "apps": [{"slug": "deploy-bot"}],
            },
            "required_linear_history": {"enabled": True},
            "block_creations": {"enabled": True},
            "required_conversation_resolution": {"enabled": False},
            "lock_branch": {"enabled": True},
            "allow_fork_syncing": {"enabled": False},
        }

        payload = protection_payload(existing)
        status = payload["required_status_checks"]
        required = {check["context"]: check for check in status["checks"]}
        self.assertTrue(status["strict"])
        self.assertEqual(required["checks-ci"]["app_id"], 12)
        self.assertEqual(required["release-gate"]["app_id"], 99)
        self.assertIn("legacy-ci", required)
        self.assertTrue(set(REQUIRED_CHECKS).issubset(required))
        self.assertEqual(payload["required_pull_request_reviews"]["required_approving_review_count"], 3)
        self.assertTrue(payload["required_pull_request_reviews"]["dismiss_stale_reviews"])
        self.assertEqual(
            payload["required_pull_request_reviews"]["dismissal_restrictions"],
            {"users": ["reviewer"], "teams": ["security"], "apps": ["review-bot"]},
        )
        self.assertEqual(
            payload["required_pull_request_reviews"]["bypass_pull_request_allowances"],
            {"users": ["release-manager"], "teams": [], "apps": []},
        )
        self.assertEqual(
            payload["restrictions"],
            {"users": ["release-manager"], "teams": ["maintainers"], "apps": ["deploy-bot"]},
        )
        self.assertTrue(payload["required_linear_history"])
        self.assertTrue(payload["block_creations"])
        self.assertTrue(payload["lock_branch"])
        self.assertFalse(payload["allow_fork_syncing"])
        self.assertTrue(payload["required_conversation_resolution"])

    def test_unrecognized_existing_actor_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "cannot safely preserve"):
            protection_payload({"restrictions": {"users": [{"id": 1}]}})

    def test_apply_reads_current_protection_before_writing(self):
        existing = {
            "required_status_checks": {"strict": True, "contexts": ["custom-release-gate"]},
            "required_pull_request_reviews": {"required_approving_review_count": 2},
        }
        calls = []

        def fake_api(method, endpoint, payload=None):
            calls.append((method, endpoint, payload))
            if method == "GET" and endpoint == "repos/example/project/branches/main/protection":
                return existing
            if method == "GET" and endpoint == "repos/example/project":
                return {"security_and_analysis": {}}
            return None

        with patch("scripts.github_admin.gh_api", side_effect=fake_api):
            apply("example/project", "main")

        self.assertEqual(calls[0][:2], ("GET", "repos/example/project/branches/main/protection"))
        self.assertEqual(calls[1][:2], ("PUT", "repos/example/project/branches/main/protection"))
        payload = calls[1][2]
        self.assertIn("custom-release-gate", payload["required_status_checks"]["contexts"])
        self.assertEqual(payload["required_pull_request_reviews"]["required_approving_review_count"], 2)


class RepositoryTargetTest(unittest.TestCase):
    def test_apply_requires_explicit_repository_target(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/github_admin.py"), "--apply"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("--repo", result.stderr)


if __name__ == "__main__":
    unittest.main()
