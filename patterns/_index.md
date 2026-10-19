# Patterns

> **Skeleton.** Patterns are **prescriptive standards**: how things SHOULD be built, with
> exact configuration, code, IaC and an actionable checklist. Domains describe what exists;
> patterns say what to do.

## Three uses

- **Build** — composing a new service from the patterns it needs.
- **Audit** — checking an existing service against the standard, via each file's checklist.
- **Onboard** — reading one pattern instead of three repos.

## Descriptive to prescriptive

```
 domains/ (here is what exists)      patterns/ (here is how to build it)
 data-and-storage.md        ───►     service/data-layer/sql-2022.md
 gcp-infrastructure.md      ───►     service/compute/cloud-run.md
 networking-and-security.md ───►     networking/psc.md
 cicd-and-deployment.md     ───►     service/cicd/deploy-pipeline.md
 observability.md           ───►     service/observability/*.md
 terraform.md               ───►     iac/*.md
```

## Holistic vs decomposed

Five **holistic** files cover a whole stack end to end and are the right entry point when
starting from nothing:

[`dotnet-service.md`](dotnet-service.md) · [`cloud-function.md`](cloud-function.md) ·
[`ado-pipeline.md`](ado-pipeline.md) · [`bash.md`](bash.md) ·
[`powershell.md`](powershell.md)

The rest are **decomposed**: one building block each, so a task that touches only caching
loads only caching. Each holistic file ends with links into the decomposed ones.

Cross-cutting (apply to all infrastructure): `iac/`, `networking/`, `security/`, `cicd/`.
Service-level (one service's building blocks): everything under `service/`.

## Composing a new service

The order matters — later choices depend on earlier ones.

```
scaffolding   repo-structure → iac-folder-layout → ado-yaml-folder → context-files
data layer    pick ONE: sql-2022 | postgresql-alloydb | mongodb-atlas | firestore
              + redis-valkey if it caches
messaging     pubsub-publisher and/or pubsub-consumer → dead-letter
docker        container-standards → dotnet-multistage
compute       cloud-run   (gce-migs and gke are maintenance-only; new work goes to Cloud Run)
networking    load-balancers → dns → cloud-armor   (+ psc if it is consumed privately)
cicd          build-pipeline → pr-validation → deploy-pipeline → multi-region-deploy
iac           terragrunt-module → terraform-module → state-management
observability datadog-apm → sentry → gcp-logging → alerting → pagerduty
security      secret-manager → iam-service-accounts → auth-auth0
```

## Index

| Area | Patterns |
| --- | --- |
| Holistic | `dotnet-service`, `cloud-function`, `ado-pipeline`, `bash`, `powershell` |
| CI/CD (cross-cutting) | `cicd/terraform-pipeline`, `cicd/image-generation`, `cicd/operational-pipeline` |
| IaC | `iac/terraform-module`, `iac/terragrunt-module`, `iac/state-management` |
| Networking | `networking/psc`, `networking/dns`, `networking/load-balancers`, `networking/cloud-armor` |
| Security | `security/secret-manager`, `security/iam-service-accounts`, `security/auth-auth0` |
| Service / scaffolding | `repo-structure`, `iac-folder-layout`, `ado-yaml-folder`, `context-files` |
| Service / compute | `cloud-run`, `gce-migs`, `gke` |
| Service / data layer | `sql-2022`, `postgresql-alloydb`, `mongodb-atlas`, `firestore`, `redis-valkey` |
| Service / messaging | `pubsub-publisher`, `pubsub-consumer`, `dead-letter` |
| Service / docker | `container-standards`, `dotnet-multistage` |
| Service / CI/CD | `build-pipeline`, `pr-validation`, `deploy-pipeline`, `multi-region-deploy` |
| Service / observability | `datadog-apm`, `sentry`, `gcp-logging`, `alerting`, `pagerduty` |

## Last Reviewed: 1970-01-01
