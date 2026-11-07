# Privileged Automation Containment

**Status: P0 containment required; no automated approval or mass secret distribution.**

## Removed from the template source

The following artifacts are retired and must not be restored:
- PAT-backed automated reviewer/approval workflow and comment helper;
- secret-dependent auto-fix workflow;
- GPG loopback wrapper used by the legacy automation;
- portfolio-wide deployment script that read a reviewer PAT from the local credential store, distributed it to repository Actions secrets, and pushed workflow changes directly to default branches;
- auto-fix loop that could commit and push repository changes directly;
- playbook describing the automated reviewer approval model.

The template retains `.github/workflows/request-independent-review.yml`. It only requests an independent review using the minimum GitHub token permission and verifies that an approval exists for the exact current PR head. It does not check out PR code, submit a review, approve, merge, or access reviewer/signing secrets.

## Required operating model

1. PR validation is secretless, read-only, and must not execute untrusted source in a job that has privileged credentials.
2. `policedbc` performs a deliberate human independent review of the exact final head.
3. `cvsz` merges only after required CI/security checks, review, CODEOWNERS, conversation resolution, and effective branch governance pass.
4. No automation may approve as `policedbc`, merge a PR, push to a protected default branch, or distribute reviewer credentials across repositories.
5. Template changes are delivered through reviewable PRs. Repository-specific deployment and secret configuration remain explicit operator actions.

## Credential incident response is separate

Deleting these source files does not revoke a previously distributed PAT, rotate a signing key, or invalidate a historical passphrase. An authorized GitHub administrator must:
- inventory repositories where the reviewer secret was configured;
- revoke/rotate the token if it was distributed or exposed;
- determine whether any signing credential was real and rotate it if necessary;
- inspect GitHub audit events and secret-scanning/history evidence privately;
- verify the old token is rejected.

Do not publish secret values, copy them into issues, or rewrite protected history as an improvised cleanup. Preserve audit evidence and use a separately approved history-recovery plan if required.

## Verification

`tests/test_privileged_automation_removed.py` is part of the standard unittest discovery used by `make validate-template`. It asserts that retired artifacts remain absent, Actions workflows/scripts do not reintroduce reviewer/GPG secrets, and the retained independent-review workflow is request-only.

Passing this source test is not credential-rotation evidence, repository-wide remediation evidence, or production-readiness evidence.
