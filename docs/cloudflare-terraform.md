# Cloudflare and Terraform ownership

New projects must **not** create their own Cloudflare Terraform. DNS records
and tunnel ingress for `*.zeaz.dev` are owned by a single repository, and that
repository is the only place they may be declared.

## The rule

| | |
|---|---|
| Owner | `zworkforce` — `infrastructure/terraform/cloudflare` |
| Scope | every `*.zeaz.dev` DNS record and the shared tunnel ingress |
| This repository may | declare application code, containers, and its own runtime configuration |
| This repository must not | contain `cloudflare_dns_record`, `cloudflare_tunnel`, `cfargotunnel.com`, or a per-project `infrastructure/terraform/cloudflare` |

Two copies of the same record is not a harmless redundancy. It produces
configuration that cannot reproduce reality, and a `plan` in the wrong
repository proposes creating records another repository already owns. That
already happened here: `zaffiliate.zeaz.dev` had a live record owned by
zworkforce and a declaration in a different repository that had never been
applied, so the two drifted apart.

## Requesting a hostname

1. Confirm the service is running and healthy on a loopback port on the
   target host.
2. Add the declaration to `zworkforce` on a feature branch, following an
   existing file such as `zksato.tf` or `llmwiki.tf`:
   - a hostname variable validated as a subdomain of the zone,
   - an origin variable validated to a loopback address, and pinned to the
     reviewed port so it cannot drift to another listener,
   - a `cloudflare_dns_record` pointing at `local.tunnel_cname`,
   - a matching entry in the tunnel ingress list,
   - a URL output.
3. Check whether a record already exists. If it does, **adopt it**:

   ```bash
   terraform import cloudflare_dns_record.<name> "<zone_id>/<record_id>"
   ```

   Importing is always correct. Creating will fail with a duplicate-record
   error, and deleting first would briefly take the hostname offline.
4. Run `terraform plan` and confirm `0 to destroy`. A plan that proposes
   destroying anything unrelated means the branch is based on a config that
   does not match the applied state. Stop and rebase; do not apply it.
5. Apply, then verify the public route and re-check the other hostnames on the
   same tunnel for regressions.
6. Open a pull request. The tunnel also serves production hostnames, so a
   careless ingress edit has a wider blast radius than the new hostname.

## If the project needs a separate tunnel

Do not create one by default. A separate tunnel means another connector, its
own credential, and another thing to keep alive across reboots. Raise it
first, and expect to justify why the shared tunnel is not sufficient.

## Local development

Terraform is not run from this project. `terraform plan` requires the operator
credentials that live in the zworkforce host configuration, and the state is
not part of this repository.
