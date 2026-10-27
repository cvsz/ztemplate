"""Static contract tests for the independent-review workflow and rollout script."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = (ROOT / ".github/workflows/request-independent-review.yml").read_text(encoding="utf-8")
ROLLOUT = (ROOT / "scripts/rollout-independent-review.sh").read_text(encoding="utf-8")


class IndependentReviewWorkflowTests(unittest.TestCase):
    def test_review_request_is_refreshed_on_head_updates(self):
        self.assertIn("synchronize", WORKFLOW)
        self.assertIn("pull_request_review:", WORKFLOW)
        self.assertIn("[submitted, dismissed]", WORKFLOW)

    def test_gate_requires_a_distinct_reviewer_on_the_exact_head(self):
        self.assertIn("verify-independent-approval:", WORKFLOW)
        self.assertIn("vars.INDEPENDENT_REVIEWER", WORKFLOW)
        self.assertIn("HEAD_SHA:", WORKFLOW)
        self.assertIn('.state == "APPROVED"', WORKFLOW)
        self.assertIn(".commit_id == $sha", WORKFLOW)
        self.assertIn("PR_AUTHOR", WORKFLOW)
        self.assertNotIn("policedbc", WORKFLOW)
        self.assertNotIn("actions/checkout", WORKFLOW)

    def test_permissions_are_scoped_and_rollout_skips_mirrors(self):
        self.assertIn("pull-requests: read", WORKFLOW)
        self.assertIn("pull-requests: write", WORKFLOW)
        self.assertIn("mirror_url", ROLLOUT)
        self.assertIn("OWNER=", ROLLOUT)
        self.assertNotIn(chr(92) + "$" + "{", ROLLOUT)
        self.assertNotIn(chr(92) + "$" + "{{", WORKFLOW)
        self.assertIn('cp "$SOURCE_WORKFLOW" "$WORKFLOW"', ROLLOUT)
        self.assertIn("INDEPENDENT_REVIEWER", ROLLOUT)
        self.assertNotIn("REVIEWER:-policedbc", ROLLOUT)

    def test_rollout_uses_authenticated_clone_for_private_repositories(self):
        self.assertIn('gh repo clone "$repo" "$repo_dir" -- --depth 1 --branch "$base"', ROLLOUT)
        self.assertNotIn('git clone --quiet --depth 1 --branch "$base" "https://github.com/$repo.git"', ROLLOUT)

    def test_rollout_selects_user_or_organization_repository_endpoint(self):
        self.assertIn("owner_type=", ROLLOUT)
        self.assertIn("Organization)", ROLLOUT)
        self.assertIn("orgs/$OWNER/repos?per_page=100&type=all", ROLLOUT)
        self.assertIn("users/$OWNER/repos?per_page=100&type=owner", ROLLOUT)


if __name__ == "__main__":
    unittest.main()
