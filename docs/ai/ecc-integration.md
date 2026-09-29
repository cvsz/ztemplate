# ECC Integration

This template includes a root `ecc-install.json` using ECC install-config schema version 1.

## Why the manifest is minimal

The template intentionally does not select a `target`, `profile`, or module set. Those choices are project- and harness-specific and should be made after a repository is created from this template.

The manifest therefore establishes a supported ECC configuration surface without forcing Claude, Codex, OpenCode, Cursor, hooks, language packs, or other runtime choices onto every generated repository.

## Upstream contract

Verified against the ECC upstream installer contract at commit:

`90dfd9505dc860714cf3cc8216ad7bbb96d93365`

Relevant upstream files:

- `scripts/lib/install/config.js` — default project config filename is `ecc-install.json`
- `schemas/ecc-install-config.schema.json` — schema version 1; only `version` is required
- `manifests/install-profiles.json` — profiles such as minimal, core, developer, security, research, and full

The schema URL in `ecc-install.json` is commit-pinned for reproducibility.

## Project setup

After creating a repository from this template, review ECC's current setup documentation and select the smallest appropriate target/profile. Do not copy a full profile merely to satisfy an audit metric.

A current guided setup may be started with:

```bash
npx ecc-universal@2.2.1 install --guided
```

Review the planned destinations and mutations before applying them.

## Drift policy

- Do not silently change the pinned schema reference.
- Re-verify upstream schema and installer behavior before updating the pin.
- Keep ECC runtime installation separate from this repository's readiness claims.
- Installing ECC components does not make a generated project production ready.
