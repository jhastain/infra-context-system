# Domains

> **Skeleton.** Cross-cutting views of the infrastructure, by concern. These answer
> "how does *X* work across the org?" They are **descriptive**: what exists today, not
> what should be built. For the latter see [`../patterns/_index.md`](../patterns/_index.md).

## When a domain file is justified

A new cross-cutting infrastructure concern that affects **3 or more services**. Below that,
add a section to an existing domain file.

## Domains

| Domain | Covers |
| --- | --- |
| [Cloud infrastructure](gcp-infrastructure.md) | Project inventory and naming, compute footprint, shared resources |
| [Networking and security](networking-and-security.md) | VPCs, subnets, firewall classes, private connectivity, DNS zones, WAF |
| [Data and storage](data-and-storage.md) | Relational, document, object, cache, messaging, secrets |
| [CI/CD and deployment](cicd-and-deployment.md) | Repos, pipelines, shared templates, promotion flow, ephemeral environments |
| [Observability](observability.md) | Metrics, error tracking, logging pipeline, alerting posture |
| [Terraform](terraform.md) | IaC repo split, module inventory, state, provider pinning, coverage |

## The deduplication rule

A domain file **summarises** and links to the system file for detail; the system file holds
the **detail** and links back here for cross-cutting context. The same table never lives in
both. When you catch yourself copying one, link instead.

## Last Reviewed: 1970-01-01
