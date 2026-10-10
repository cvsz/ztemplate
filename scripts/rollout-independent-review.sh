#!/usr/bin/env bash
# Roll out independent review workflow to all repositories owned by cvsz.
# Requires: gh, git, jq, and gh auth with repo/workflow permissions.
set -euo pipefail
OWNER="${OWNER:-cvsz}"
REVIEWER="${REVIEWER:-policedbc}"
APPLY="${APPLY:-0}"
WORKFLOW=".github/workflows/request-independent-review.yml"
BRANCH="chore/independent-review-governance"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
gh api --paginate "users/$OWNER/repos?per_page=100&type=owner" --jq '.[] | [.full_name, .default_branch, .archived, .fork, .disabled] | @tsv' |
while IFS=$'\t' read -r repo base archived fork disabled; do
  if [[ "$archived" == true || "$fork" == true || "$disabled" == true ]]; then
    printf 'SKIP %s (archived/fork/disabled)\n' "$repo"; continue
  fi
  if ! gh api "repos/$repo/collaborators/$REVIEWER/permission" --jq '.permission' 2>/dev/null | grep -Eq '^(write|maintain|admin)$'; then
    printf 'BLOCKED %s (reviewer lacks write access)\n' "$repo"; continue
  fi
  if gh api "repos/$repo/contents/$WORKFLOW?ref=$base" >/dev/null 2>&1; then
    printf 'SKIP %s (workflow already exists; review manually)\n' "$repo"; continue
  fi
  if gh api "repos/$repo/branches/$BRANCH" >/dev/null 2>&1; then
    printf 'SKIP %s (rollout branch already exists)\n' "$repo"; continue
  fi
  printf 'READY %s base=%s\n' "$repo" "$base"
  [[ "$APPLY" == 1 ]] || continue
  mkdir -p "$TMP/repo"; rm -rf "$TMP/repo"; mkdir -p "$TMP/repo"
  git clone --quiet --depth 1 --branch "$base" "https://github.com/$repo.git" "$TMP/repo"
  ( cd "$TMP/repo"
    git checkout -q -b "$BRANCH"
    mkdir -p .github/workflows
    cat > "$WORKFLOW" <<'YAML'
name: Request independent PR review
on:
  pull_request_target:
    types: [opened, reopened, ready_for_review]
permissions:
  contents: read
  pull-requests: write
jobs:
  request-review:
    if: github.event.pull_request.draft == false && github.event.pull_request.user.login != 'policedbc'
    runs-on: ubuntu-latest
    steps:
      - name: Request policedbc review
        env:
          GH_TOKEN: ${{ github.token }}
          GH_REPO: ${{ github.repository }}
          PR_NUMBER: ${{ github.event.pull_request.number }}
        run: |
          set -euo pipefail
          gh api --method POST "repos/$GH_REPO/pulls/$PR_NUMBER/requested_reviewers" -f 'reviewers[]=policedbc'
YAML
    git add "$WORKFLOW"
    git commit -qm "ci: request independent policedbc PR review"
    git push -q -u origin "$BRANCH"
  )
  gh pr create -R "$repo" --head "$BRANCH" --base "$base" \
    --title "ci: request independent policedbc PR review" \
    --body "Automated review request only. Requires policedbc approval and existing required CI checks; does not approve, merge, or bypass branch rules."
  printf 'PR CREATED %s\n' "$repo"
done
echo "NOTE: Configure required reviews, stale approval dismissal, and branch rulesets separately per repository."
