# MASTER PROMPT — GitHub Repository Production Configuration & Governance

Target repository:

`cvsz/ztemplate`

## Mission

Inspect, audit, configure, harden, document, and verify every GitHub repository-level capability that is useful for this project and available through the current GitHub account, GitHub App connection, GitHub API, GitHub CLI, repository files, or GitHub Settings UI.

The final repository should have a coherent production-ready GitHub configuration without weakening existing security controls, deleting valid project history, duplicating existing workflows, exposing secrets, or inventing credentials.

Operate incrementally and evidence-first.

Do not claim a feature is configured unless it is directly verified.

---

# 1. Inspect Current Repository State First

Before changing anything, inspect and record:

* repository visibility
* repository owner
* default branch
* repository permissions available to the authenticated account/app
* repository description
* homepage URL
* topics
* template-repository status
* archived status
* fork status
* merge methods
* auto-merge
* branch update behavior
* squash merge configuration
* issue support
* projects support
* Wiki
* Discussions
* Pages
* Releases
* Packages
* Actions
* environments
* deployment protection
* branch protection/rulesets
* CODEOWNERS
* security policy
* Dependabot
* dependency graph
* secret scanning
* push protection
* private vulnerability reporting
* code scanning / CodeQL
* Actions permissions
* workflow permissions
* GitHub Apps installed on the repository
* webhooks
* repository secrets
* repository variables
* environment secrets
* environment variables
* existing workflows
* reusable workflows
* release workflows
* Pages workflows
* deployment workflows
* scheduled workflows
* social preview
* repository metadata files
* community health files
* issue templates
* PR templates
* release templates
* GitHub funding configuration
* SECURITY.md
* SUPPORT.md
* CONTRIBUTING.md
* CODE_OF_CONDUCT.md
* GOVERNANCE.md
* CHANGELOG.md
* LICENSE
* AGENTS.md
* automation/developer instructions

Produce a current-state matrix:

| Capability | Current State | Desired State | Action | Evidence |
| ---------- | ------------- | ------------- | ------ | -------- |

Do not change a setting merely because it exists.

---

# 2. Preserve Existing Repository Behavior

Before implementing changes:

1. Inventory all `.github/workflows/*.yml` and `.yaml`.
2. Identify duplicated workflows.
3. Identify obsolete workflow files.
4. Identify overlapping triggers.
5. Identify workflows that use deprecated GitHub Actions.
6. Identify workflows with excessive permissions.
7. Identify secrets referenced by workflows.
8. Identify variables referenced by workflows.
9. Identify environment names referenced by deployments.
10. Identify artifacts, Pages deployment, containers, packages, and release dependencies.

Prefer updating/reusing an existing workflow over adding another workflow with the same responsibility.

Do not delete an existing workflow unless its replacement is verified and its removal is explicitly justified.

---

# 3. GitHub Apps

Audit GitHub Apps installed on the repository/account.

For each app record:

* app name
* installation scope
* repository access
* permissions requested
* events subscribed
* whether the permission is actually required
* security impact
* operational purpose
* whether it should remain enabled

Apply least privilege.

Recommended classes to evaluate when actually useful:

* GitHub Actions
* Dependabot
* CodeQL / code scanning
* Renovate if intentionally used
* deployment platform app
* monitoring/observability app
* issue/project automation
* release automation
* dependency/security automation

Do NOT install arbitrary apps simply to increase the app count.

Do NOT grant administration, secrets, contents-write, actions-write, deployments-write, or organization-wide access unless technically required.

Record denied/unnecessary permissions.

---

# 4. Repository Secrets and Variables

Audit every workflow reference to:

`${{ secrets.* }}`

and:

`${{ vars.* }}`

Build:

`docs/github/SECRETS-AND-VARIABLES.md`

Document names only.

NEVER write actual secret values to source control, logs, PR descriptions, issues, documentation, or generated artifacts.

Classify each item as:

* repository secret
* environment secret
* organization secret
* repository variable
* environment variable
* GitHub-provided token
* external secret manager reference

For every secret define:

* purpose
* consuming workflow
* environment
* required/optional
* rotation owner
* rotation expectation
* least-privilege scope

Do not fabricate unavailable secret values.

If a required secret is missing, report:

`REQUIRES OWNER-SUPPLIED SECRET`

instead of inventing one.

---

# 5. GitHub Environments

Create or reconcile only environments that have an actual deployment purpose.

Preferred model where applicable:

* `development`
* `staging`
* `production`

For production:

* configure deployment branch/tag restrictions
* require explicit approval where supported and useful
* apply wait timers only when justified
* isolate production secrets from repository-level secrets
* restrict production credentials
* prevent pull requests from untrusted forks from accessing protected secrets
* ensure deployments use explicit `environment: production`

For staging:

* use independent credentials
* never reuse privileged production credentials unless unavoidable and documented

For development:

* prefer non-sensitive/mock credentials

Document all environments in:

`docs/github/ENVIRONMENTS.md`

---

# 6. GitHub Actions Security

Audit every workflow.

Use explicit top-level or job-level `permissions:`.

Default toward:

```yaml
permissions:
  contents: read
```

Grant additional permissions only to jobs that require them.

Examples:

```yaml
permissions:
  contents: read
  security-events: write
```

or:

```yaml
permissions:
  contents: read
  packages: write
```

Avoid:

```yaml
permissions: write-all
```

unless unavoidable and explicitly justified.

Validate:

* fork PR safety
* `pull_request_target`
* secret exposure
* shell injection
* expression injection
* artifact poisoning
* cache poisoning
* untrusted checkout execution
* release token scope
* deployment credentials
* mutable action tags
* third-party Actions provenance
* artifact retention
* workflow concurrency
* cancellation
* timeout limits

Pin security-sensitive third-party Actions to immutable commit SHAs when practical.

---

# 7. Standard CI Workflow Set

Reuse existing workflows where possible.

Ensure equivalent verified coverage exists for:

### CI

* dependency installation
* lint
* formatting validation
* unit tests
* integration tests where appropriate
* build
* package validation

### Security

* CodeQL
* dependency review where supported
* secret scanning
* dependency vulnerability scanning
* SAST
* license policy where applicable

### Release

* tagged release validation
* release artifact generation
* checksums
* SBOM
* provenance/attestation where supported
* immutable release behavior

### Container

When containers exist:

* build
* vulnerability scanning
* non-root validation
* immutable image tags/digests
* SBOM
* publish only from trusted refs

### Documentation

* Markdown validation where useful
* broken-link validation where useful
* Pages build verification

Do not add meaningless CI jobs merely for checklist completeness.

---

# 8. Dependabot / Dependency Automation

Configure or reconcile `.github/dependabot.yml`.

Cover only package ecosystems actually present.

Possible ecosystems:

* npm
* pip
* github-actions
* docker
* gomod
* cargo
* maven
* gradle

Use grouped updates where appropriate.

Avoid excessive PR churn.

Do not automatically merge breaking major versions without explicit compatibility evidence.

---

# 9. Branch Rules / Rulesets

Audit existing branch protection and repository rulesets.

For `main`, configure equivalent protection where repository capabilities permit:

* pull request required
* required status checks
* stale approvals handling as appropriate
* conversation resolution
* prevent accidental force-push
* prevent deletion
* signed commits where project policy requires it
* linear history only if compatible with repository merge strategy

Required checks must correspond to real workflow jobs.

Never configure a nonexistent required status check.

Do not lock administrators out without a verified recovery path.

---

# 10. Webhooks

Audit existing repository webhooks.

For each webhook validate:

* target purpose
* event subscriptions
* active/inactive state
* TLS verification
* secret configured
* least event scope
* retry/error handling
* duplicate webhook delivery behavior
* idempotency expectation

Never expose webhook secrets.

Do not create webhook endpoints without an actual target URL supplied or already documented.

For missing external endpoints report:

`BLOCKED: WEBHOOK TARGET NOT PROVIDED`

rather than inventing an endpoint.

---

# 11. GitHub Pages

Audit whether Pages is useful for this repository.

If existing static documentation/site assets justify Pages:

* configure Pages source intentionally
* prefer GitHub Actions deployment where appropriate
* validate build
* validate asset paths
* validate SPA routing if applicable
* enforce HTTPS
* document custom-domain requirements
* configure `CNAME` only when a real domain is supplied

Do not invent a custom domain.

Ensure Pages deployment cannot expose repository secrets or internal artifacts.

---

# 12. Wiki

Enable and initialize Wiki when appropriate.

The Wiki should complement repository docs rather than duplicate source-of-truth technical specifications.

Suggested Wiki structure:

* Home
* Getting Started
* Architecture
* Development
* Deployment
* Configuration
* Security
* Operations
* Troubleshooting
* FAQ
* Release Process
* Contributing

Repository-controlled docs remain canonical for versioned engineering specifications.

Wiki pages should link to canonical files rather than silently diverging.

---

# 13. Discussions

Enable GitHub Discussions if suitable.

Recommended categories:

* Announcements
* General
* Ideas
* Q&A
* Show and Tell
* Development
* Support

Define moderation expectations.

Use Discussions for community collaboration.

Do not use Discussions as a substitute for:

* security reports
* confirmed bugs requiring tracking
* release blockers
* confidential support

Direct vulnerability reports to SECURITY.md/private vulnerability reporting.

---

# 14. Issues

Enable Issues where appropriate.

Create/reconcile templates:

`.github/ISSUE_TEMPLATE/bug_report.yml`

`.github/ISSUE_TEMPLATE/feature_request.yml`

`.github/ISSUE_TEMPLATE/security.yml`

`.github/ISSUE_TEMPLATE/config.yml`

Templates should request:

* environment
* version/commit
* reproduction steps
* expected behavior
* actual behavior
* logs with secrets removed
* severity where relevant

Security template must redirect sensitive vulnerabilities away from public issues.

---

# 15. Pull Request Governance

Ensure `.github/pull_request_template.md` exists and reflects actual repository requirements.

Include:

* summary
* scope
* changed subsystems
* testing
* security implications
* backwards compatibility
* migration implications
* documentation
* deployment impact
* rollback
* checklist

Do not hard-code stale test counts.

---

# 16. CODEOWNERS

Create/reconcile `.github/CODEOWNERS`.

Assign ownership only to valid GitHub users/teams.

Protect sensitive areas where applicable:

* `.github/workflows/`
* security configuration
* deployment configuration
* infrastructure
* authentication/authorization
* secrets-related documentation
* release configuration

Do not invent users or teams.

---

# 17. Community Health Files

Audit/create as appropriate:

* README.md
* LICENSE
* SECURITY.md
* SUPPORT.md
* CONTRIBUTING.md
* CODE_OF_CONDUCT.md
* GOVERNANCE.md
* CHANGELOG.md
* AUTHORS.md / CONTRIBUTORS.md when justified

Avoid duplicate or stale documents.

---

# 18. Repository Metadata

Reconcile:

* repository description
* homepage
* topics
* About section
* releases
* packages
* deployments

Use accurate project terminology only.

Do not claim production readiness unless verified.

---

# 19. Social Preview

Prepare a repository social preview image specification.

Preferred dimensions:

`1280 × 640`

Minimum:

`640 × 320`

Design should include:

* project name: `zAnything`
* concise project purpose
* high-contrast readable typography
* GitHub/social-card safe margins
* project branding
* no secret/internal information
* no misleading badges

Store source artwork in a documented project asset location if repository policy permits.

If repository settings API cannot upload the social preview directly, generate the final PNG and report the exact manual upload path:

`Settings → General → Social preview → Edit → Upload image`

Do not claim it was uploaded unless verified.

---

# 20. Releases

Audit release behavior.

Where applicable configure:

* semantic versioning
* release notes
* changelog
* tagged builds
* artifact checksums
* SBOM
* provenance
* release immutability
* release validation workflow

Do not publish a release merely to test configuration.

---

# 21. Security Settings

Enable/configure every supported security control that is appropriate and available:

* dependency graph
* Dependabot alerts
* Dependabot security updates
* CodeQL
* secret scanning
* push protection
* private vulnerability reporting
* security policy
* dependency review
* signed release artifacts where applicable

If a feature requires GitHub Advanced Security or another plan not available, mark:

`UNAVAILABLE ON CURRENT GITHUB PLAN`

Do not simulate the setting.

---

# 22. Actions Policy

Audit:

* allowed Actions policy
* reusable workflow usage
* GitHub-owned Actions
* verified creator Actions
* third-party Actions
* SHA pinning

Prefer GitHub-owned or verified actions.

Restrict arbitrary actions when practical without breaking required workflows.

---

# 23. Artifact Policy

For each workflow artifact specify:

* name
* purpose
* retention period
* sensitivity
* release vs temporary artifact
* integrity requirements

Never upload:

* `.env`
* API keys
* SSH keys
* credentials
* tokens
* raw secret-bearing logs
* private configuration

---

# 24. Caching

Audit caches for:

* dependency poisoning
* excessive scope
* privileged branch reuse
* cross-PR contamination

Use deterministic cache keys.

Do not restore untrusted caches into privileged release jobs without appropriate isolation.

---

# 25. Web Security Headers / Pages

If GitHub Pages hosts an application/documentation site, inspect whether the deployment architecture supports required browser security measures.

Document limitations where GitHub Pages itself cannot supply custom response headers.

Do not claim unsupported headers are enabled.

---

# 26. Deployment Governance

Every production deployment workflow should provide:

* environment binding
* explicit source SHA
* artifact identity
* deployment record
* approval boundary where applicable
* health verification
* rollback method
* concurrency control
* timeout
* failure handling

Never deploy from an untrusted PR context.

---

# 27. GitHub App / Token Credential Model

Document which authentication mechanism each automation uses:

* `GITHUB_TOKEN`
* GitHub App installation token
* PAT
* OIDC
* deployment-provider credential

Prefer:

1. `GITHUB_TOKEN`
2. OIDC
3. scoped GitHub App token
4. narrowly scoped external credential

Avoid long-lived PATs where modern alternatives exist.

---

# 28. OIDC

Where cloud/deployment providers support GitHub OIDC:

prefer OIDC over stored long-lived cloud credentials.

Restrict trust policy by:

* repository
* branch/tag
* environment
* workflow

Do not configure an OIDC provider without actual external provider details.

---

# 29. Repository Automation Documentation

Create:

`docs/github/README.md`

with links to:

* repository settings inventory
* environments
* secrets/variables names
* workflow architecture
* release process
* security controls
* Pages
* Wiki
* Discussions
* webhook architecture
* GitHub Apps
* branch/ruleset policy
* incident/recovery notes

---

# 30. Repository Configuration Evidence

Create:

`docs/github/CONFIGURATION-MATRIX.md`

Use:

| Area | Desired | Actual | Evidence | Gap | Owner Action |
| ---- | ------- | ------ | -------- | --- | ------------ |

Never mark an item complete without evidence.

---

# 31. Missing Configuration Detection

After the primary audit, actively search for missing capabilities including:

* missing CI coverage
* missing security workflow
* missing dependency automation
* missing environment separation
* missing production approval
* missing CODEOWNERS
* missing release automation
* missing rollback evidence
* missing Pages deployment
* missing documentation
* missing secret references
* stale secret names
* unused variables
* broken badges
* stale workflow versions
* unsupported action runtime versions
* dead links
* obsolete templates
* duplicate configuration
* missing license headers where required
* missing SBOM
* missing provenance
* missing artifact checksums
* missing release evidence
* missing recovery documentation

Classify gaps:

* CRITICAL
* HIGH
* MEDIUM
* LOW
* OPTIONAL

Do not inflate severity.

---

# 32. Existing Repository-Specific Constraint

For `cvsz/zanything`, inspect existing workflows before creating new ones.

Known repository evidence indicates that CI already exists under `.github/workflows/ci.yml` and a static-site workflow exists under `.github/workflows/static.yml`.

Do not duplicate those responsibilities.

Reconcile and improve them in place when safe.

---

# 33. Changes Through Pull Requests

For source-controlled configuration:

1. branch from current exact `main`
2. make one bounded logical change set
3. run/observe tests and Actions
4. open a PR
5. inspect changed files
6. inspect review threads
7. inspect exact-head workflow runs
8. fix failures
9. rerun only failed workflows when appropriate
10. merge only when required checks are green and blockers are resolved

Never force-merge a red or stale PR.

---

# 34. Administrative Settings

For settings that the connected GitHub App/API cannot modify:

produce an exact owner-action checklist.

Example:

```text
OWNER ACTION REQUIRED
Repository: cvsz/zanything
Path: Settings → Secrets and variables → Actions
Action: Create repository secret
Name: EXAMPLE_TOKEN
Value: supply externally
Reason: required by <workflow>
```

Do not pretend unsupported settings were configured.

---

# 35. Secret Handling Rule

Never:

* print secret values
* commit secret values
* request the user to paste production secrets into public issues
* put secrets into PR bodies
* put secrets into generated screenshots
* put secrets into test fixtures
* echo secrets during Actions

Use GitHub secret masking appropriately.

---

# 36. Never Perform Destructive Repository Operations

Do not:

* archive repository
* delete repository
* rename repository
* transfer repository
* delete unrelated branches
* delete releases
* delete packages
* rewrite history
* force-push protected branches

unless separately and explicitly authorized.

---

# 37. Verification

Before claiming completion verify:

* all changed workflows parse successfully
* required CI is green on exact head
* no unresolved review threads
* security controls were not weakened
* no secrets were introduced into git history
* Pages deploy succeeds if configured
* release workflow is safe if changed
* environments align with workflows
* documented secrets match workflow references
* unused secret references are removed or documented
* webhooks are active only when valid targets exist
* Discussions/Wiki state matches documentation
* branch protection/rulesets reference actual checks
* social preview asset meets dimensions
* repository metadata is accurate

---

# 38. Final Report

Return:

## Repository

`cvsz/zanything`

## Exact HEAD

`<sha>`

## Configured

List only verified completed items.

## Existing / Preserved

List existing features intentionally retained.

## Changed

List exact settings/files/workflows changed.

## GitHub Apps

List app status and least-privilege decisions.

## Environments

List environments and protection.

## Secrets

List secret NAMES only.

Never values.

## Variables

List names and scopes.

## Workflows

List workflows and status.

## Webhooks

List configured webhook purpose/event scope without secrets.

## Pages

Report verified Pages state and URL if available.

## Wiki

Report state.

## Discussions

Report state/categories.

## Social Preview

Report dimensions and upload state.

## Security

Report actual enabled controls.

## CI Evidence

For every changed PR report:

* PR number
* exact head SHA
* required checks
* success/failure
* unresolved review threads

## Blockers

State exact owner/admin/external-provider action required.

## Missing

List remaining genuine gaps.

## Next Action

Give the smallest safe next action.

If everything available within current permissions is complete, say:

`All repository configuration actions available through the current GitHub permissions are complete.`

Do not invent further work solely to keep the project active.
