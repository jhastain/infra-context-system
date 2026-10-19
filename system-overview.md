# System overview

> **Skeleton.** This is L1 — the only file that is always loaded. In a filled-in copy it is
> the system map plus the routing table below, kept under ~800 tokens so loading it is never
> a decision. Replace the bracketed placeholders with your own estate.

## STOP — Load context before writing code (MANDATORY)

**You MUST load the relevant context files below BEFORE writing any code, pipeline YAML,
Terraform, scripts, or infrastructure configuration. NEVER generate infrastructure or
pipeline code from training data alone. Verify against the org-specific patterns first.
There are no exceptions.**

**Multiple matches = load ALL matching files.**

| Keywords in the task | MUST load |
| --- | --- |
| cloud run, container, service deploy | `patterns/service/compute/cloud-run.md` |
| VM, instance group, MIG, autoscaling | `patterns/service/compute/gce-migs.md` |
| kubernetes, GKE, helm, node pool | `patterns/service/compute/gke.md` |
| SQL Server, Cloud SQL, MSSQL, migrations | `patterns/service/data-layer/sql-2022.md` |
| postgres, AlloyDB, alembic | `patterns/service/data-layer/postgresql-alloydb.md` |
| mongo, atlas, document store | `patterns/service/data-layer/mongodb-atlas.md` |
| firestore, collection, document db | `patterns/service/data-layer/firestore.md` |
| redis, valkey, memorystore, cache | `patterns/service/data-layer/redis-valkey.md` |
| pub/sub, publish, topic | `patterns/service/messaging/pubsub-publisher.md` |
| subscriber, consumer, message handler | `patterns/service/messaging/pubsub-consumer.md` |
| dead letter, DLQ, poison message, large message | `patterns/service/messaging/dead-letter.md` |
| dockerfile, image, base image, registry | `patterns/service/docker/container-standards.md` |
| multistage, build args, layer cache | `patterns/service/docker/dotnet-multistage.md` |
| build pipeline, CI, compile, unit tests in CI | `patterns/service/cicd/build-pipeline.md` |
| deploy pipeline, promotion, manual gate | `patterns/service/cicd/deploy-pipeline.md` |
| PR validation, pre-merge checks | `patterns/service/cicd/pr-validation.md` |
| multi-region, failover, DR | `patterns/service/cicd/multi-region-deploy.md` |
| APM, tracing, spans | `patterns/service/observability/datadog-apm.md` |
| error tracking, exceptions, issue grouping | `patterns/service/observability/sentry.md` |
| structured logging, log levels, redaction | `patterns/service/observability/gcp-logging.md` |
| alerting, monitor, SLO, uptime check | `patterns/service/observability/alerting.md` |
| on-call, paging, escalation, incident routing | `patterns/service/observability/pagerduty.md` |
| terraform module, versioning, module source | `patterns/iac/terraform-module.md` |
| terragrunt, hcl, environment hierarchy | `patterns/iac/terragrunt-module.md` |
| remote state, backend, state bucket | `patterns/iac/state-management.md` |
| terraform pipeline, plan, apply | `patterns/cicd/terraform-pipeline.md` |
| packer, image build, golden image | `patterns/cicd/image-generation.md` |
| scheduled job, cleanup, maintenance pipeline | `patterns/cicd/operational-pipeline.md` |
| private service connect, PSC, endpoint | `patterns/networking/psc.md` |
| DNS, zone, record, domain | `patterns/networking/dns.md` |
| load balancer, backend service, NEG, SSL cert | `patterns/networking/load-balancers.md` |
| WAF, cloud armor, rate limit, blocked IP | `patterns/networking/cloud-armor.md` |
| secret, key rotation, secret manager | `patterns/security/secret-manager.md` |
| IAM, service account, role, impersonation | `patterns/security/iam-service-accounts.md` |
| auth, JWT, bearer token, authorize | `patterns/security/auth-auth0.md` |
| new repo, project layout, solution structure | `patterns/service/service-scaffolding/repo-structure.md` |
| IaC folder, where does this resource go | `patterns/service/service-scaffolding/iac-folder-layout.md` |
| pipeline folder, YAML layout | `patterns/service/service-scaffolding/ado-yaml-folder.md` |
| CLAUDE.md, agent context, rules file | `patterns/service/service-scaffolding/context-files.md` |
| bash, shell script | `patterns/bash.md` |
| powershell, ps1 | `patterns/powershell.md` |
| new .NET service, end to end | `patterns/dotnet-service.md` |
| cloud function, serverless handler | `patterns/cloud-function.md` |
| pipeline authoring, templates, stages | `patterns/ado-pipeline.md` |
| "which project / which service is X" | `service-catalog.md` |
| monitoring estate, what alerts exist | `domains/observability.md` |
| networking estate, VPC, subnets, firewall | `domains/networking-and-security.md` |
| data estate, what databases exist | `domains/data-and-storage.md` |
| deployment estate, what pipelines exist | `domains/cicd-and-deployment.md` |
| cloud estate, what projects exist | `domains/gcp-infrastructure.md` |
| IaC estate, which repos hold what | `domains/terraform.md` |

## System map

<!--
Replace with yours. A short ASCII request-flow diagram plus a scale line, e.g.:

  internet ─▶ [WAF] ─▶ [LB] ─▶ [edge service] ─┬─▶ [monolith] ─▶ [SQL primary]
                                               └─▶ [microservices] ─▶ [Pub/Sub]

  Scale: N cloud projects, N services, N pipelines, N databases.

Keep it under ten lines. Anything longer belongs in a domain file.
-->

## Services

<!--
A compact table, one row per service: name, what it does, where it runs, who owns it.
Enough for an agent to pick the right deeper file. Full detail lives in service-catalog.md.
-->

## Wiki

<!-- Table: Section | Topic | Link. The authoritative pages this tree summarises. -->

## Last Reviewed: 1970-01-01
