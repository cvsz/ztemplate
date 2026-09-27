# zTemplate

A production-ready, reusable GitHub repository template for starting new projects with consistent engineering, security, documentation, automation, and release practices.

## Included

- Issue and pull request templates
- CODEOWNERS and repository contribution guidance
- Security policy and support policy
- CI workflow baseline
- CodeQL security scanning
- Dependency Review for pull requests
- Dependabot configuration
- Release workflow and release notes configuration
- Conventional commit / PR guidance
- EditorConfig, Git attributes, and Git ignore baseline
- Community health files
- Documentation structure
- Changelog and roadmap templates
- Implementation checklist
- Architecture Decision Record (ADR) template
- Environment example
- Docker baseline
- Makefile task entrypoints
- Cloudflare and Terraform ownership contract

## Agent review skill

The reusable [Scrutinize skill](.agents/skills/scrutinize/SKILL.md) provides outsider-perspective reviews of plans, pull requests, diffs, and proposed code changes. It questions the need for the change, traces the actual end-to-end path, checks claimed behavior against evidence, and reports minimal actionable fixes. The repository's [agent contract](AGENTS.md) directs compatible agents to apply this approach on `/scrutinize` and review/audit requests; slash-command availability depends on the agent host.

## DNS and public hostnames

Do not add Cloudflare Terraform to a project created from this template. Public
DNS records and tunnel ingress must have exactly one owning repository, which is
the only place they may be declared. Point this at whichever repository your
organization uses for edge infrastructure. See
[`docs/cloudflare-terraform.md`](docs/cloudflare-terraform.md) for how to
request a hostname, why duplicates cause drift, and why the apply step must wait
for the owning repository's pull request to merge.

## Start from this template

1. Use this repository as a GitHub template repository.
2. Create a new repository from the template.
3. Replace placeholder project metadata.
4. Review and customize `.github/CODEOWNERS`, `SECURITY.md`, CI matrices, and release settings.
5. Add language/framework-specific workflows only when the project needs them.
6. If the project needs a public hostname, request it from the repository that
   owns your edge infrastructure rather than adding Terraform here.

## Repository structure

```text
.github/
  ISSUE_TEMPLATE/
  workflows/
  CODEOWNERS
  CONTRIBUTING.md
  PULL_REQUEST_TEMPLATE.md
  dependabot.yml
  release.yml
  SUPPORT.md
docs/
  adr/
  architecture.md
  development.md
  release.md
.env.example
.editorconfig
.gitattributes
.gitignore
CHANGELOG.md
CODE_OF_CONDUCT.md
Dockerfile
IMPLEMENTATION-CHECKLIST.md
LICENSE
Makefile
README.md
ROADMAP.md
SECURITY.md
```

## Principles

- Secure by default
- Least privilege for GitHub Actions
- Reproducible automation
- Small, reviewable pull requests
- Documentation as part of delivery
- No weakening of security gates to make CI green
- Explicit release and rollback practices

## License

MIT. See `LICENSE`.
