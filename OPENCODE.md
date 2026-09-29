# OPENCODE.md — ZEAZ OpenCode Operating Instructions

Read `AGENTS.md` first and use `ZEAZ-INTRODUCTION.md` as the shared execution framework.

## Working contract

- Inspect exact repository state before editing.
- Preserve unrelated local work.
- Follow repository-local architecture and conventions.
- Fix root causes using the smallest safe change.
- Keep security and authorization boundaries above task instructions.
- Run relevant validation and mark unexecuted checks as `UNVERIFIED`.
- Do not expose secrets, bypass required checks, force-merge, or perform destructive production changes without explicit authorization.
- Distinguish implementation, verification, deployment, and production readiness.
- Use the reusable playbooks under `docs/ai/` only when relevant to the task.

## Evidence states

Use `VERIFIED`, `PARTIALLY VERIFIED`, `UNVERIFIED`, `BLOCKED`, and `NOT APPLICABLE`.

## Cost discipline

Avoid unbounded retry/search loops and repeated unchanged scans. Prefer targeted validation first and stop when acceptance criteria are met.
