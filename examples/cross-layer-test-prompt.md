# Cross-layer routing eval

> **Skeleton.** The routing table in `system-overview.md` is a claim: that a task mentioning
> certain words causes certain files to load. This is how you check it, because the failure
> mode is silent — the agent produces plausible code having loaded nothing.

## The test

Give an agent only `system-overview.md` and a tool that can read files from this repo, then
give it a task that **deliberately crosses layers**: it should need the catalog to identify
a service, a domain file for current state, and two or more patterns to build with.

A worked shape:

> "Add a scheduled job to `<service>` that reads from `<its database>`, publishes a summary
> to a new Pub/Sub topic, and alerts the on-call rotation if it fails. Follow our standards."

That one sentence should pull in: the catalog row (which database, which project), the
CI/CD domain (how scheduled work runs here), and the messaging, data-layer, alerting and
on-call patterns.

## Expected context flow

| Step | Trigger in the prompt | Should load | Layer |
| --- | --- | --- | --- |
| 1 | the service name | `service-catalog.md` | L2 |
| 2 | "scheduled job" | `patterns/cicd/operational-pipeline.md` | L2 |
| 3 | "reads from <database>" | the matching `patterns/service/data-layer/*.md` | L2 |
| 4 | "publishes to Pub/Sub" | `patterns/service/messaging/pubsub-publisher.md` | L2 |
| 5 | "new topic" | `patterns/iac/terragrunt-module.md` | L2 |
| 6 | "alerts" | `patterns/service/observability/alerting.md` | L2 |
| 7 | "on-call" | `patterns/service/observability/pagerduty.md` | L2 |
| 8 | "follow our standards" | the service's own `standards.md` | L3 |

## Scoring

1. **Routing completeness** — were all expected files loaded? Which were missed?
2. **No over-loading** — did it pull in files the task did not need, burning budget?
3. **Convention adherence** — does the output follow the loaded patterns, or does it look
   like generic training-data code wearing the right names?
4. **Gap honesty** — where a pattern was silent, did the agent say so, or invent?
5. **Ordering** — did it read the catalog before deciding which data-layer pattern applied?

A miss on (1) is usually a missing keyword row in the routing table, not an agent failure.
Fix the table and re-run; that is what the eval is for.

## Last Reviewed: 1970-01-01
