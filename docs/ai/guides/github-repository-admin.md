# GitHub Repository Administration Gate

Repository files alone cannot enforce GitHub branch protection or repository-level security settings. This gate must be applied through a GitHub identity with **Administration** permission.

## Automated operator path

The repository includes an idempotent helper:

```bash
python3 scripts/github_admin.py --repo OWNER/REPO
```

The default invocation is dry-run only.

Apply and immediately verify:

```bash
python3 scripts/github_admin.py --repo OWNER/REPO --apply
```

Verify without mutation:

```bash
python3 scripts/github_admin.py --repo OWNER/REPO --verify
```

Requirements:

- GitHub CLI (`gh`)
- `gh auth login`
- repository Administration permission
- an explicit `--repo OWNER/REPO` target; the helper has no repository default

Before updating classic branch protection, the helper reads the current settings and retains existing required checks, push restrictions, review counts, reviewer/bypass actors, linear-history and branch-lock settings. It then adds the template baseline. If the existing protection response contains an actor it cannot identify, the helper stops before applying changes.

## Enforced policy

The helper configures `main` to require:

- pull requests before merge;
- at least one approving review;
- stale-review dismissal;
- CODEOWNERS approval;
- approval after the latest push;
- conversation resolution;
- strict/up-to-date required status checks;
- `repository-baseline`;
- `Analyze GitHub Actions`;
- `dependency-review`;
- administrator enforcement;
- no force pushes;
- no branch deletion.

It also enables or verifies:

- Dependabot vulnerability alerts;
- automated security fixes;
- private vulnerability reporting;
- secret scanning;
- secret scanning push protection;
- read-only default Actions `GITHUB_TOKEN` permission;
- Actions cannot approve pull requests.

## Evidence rule

A successful script run is operational evidence only when the final verification step reads the effective settings back from GitHub and exits successfully.

Do not close the production-readiness gate from the presence of this script alone.

If GitHub does not expose a requested security feature for the repository plan or ownership model, classify that control according to `ZEAZ-INTRODUCTION.md` rather than silently treating it as enabled.
