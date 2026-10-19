# Service catalog

> **Skeleton.** L2 structured lookup. Optimised for scanning and cross-referencing, not for
> reading. One row per service in the index, then one metadata block per service.
>
> A **standard** service belongs here and nowhere else: this row plus the relevant pattern
> fully explains it. Only a service that breaks the pattern earns a file in `systems/`.

## Index

<!--
One row per service. Keep it to the columns an agent needs to route a question:

| Service | Type | Cloud project | Hosting | Regions | Owner |
| --- | --- | --- | --- | --- | --- |
| example-api | .NET API | example-prod-project | Cloud Run | us-central1, us-west1 | Platform |
-->

| Service | Type | Cloud project | Hosting | Regions | Owner |
| --- | --- | --- | --- | --- | --- |
| `<service>` | `<runtime>` | `<project-id>` | `<Cloud Run / GKE / MIG>` | `<regions>` | `<team>` |

## Per-service detail

<!--
Repeat this block per service. Every field is a thing an agent is asked to look up, so
keep the key names identical across services - an agent greps for "Sentry project:".

### <service-name>

- **Repo:** <repo>
- **Pipeline:** <pipeline name>
- **Database:** <engine, instance, how it connects>
- **Cache:** <instance, or none>
- **Messaging:** <topics published / subscribed>
- **Datadog service tag:** <tag>
- **Sentry project:** <slug>
- **On-call service:** <routing target>
- **Depends on:** <services>
- **Depended on by:** <services>
- **Pattern:** <relative link to the pattern that explains it>
-->

## Dependency map

<!--
Which service calls which. A small Mermaid graph or an indented list. This is the section
most often asked for and least often maintained; if it is stale, say so with a date rather
than deleting it.
-->

## Wiki references

<!-- Table: Page | Topic | Link. -->

## Last Reviewed: 1970-01-01
