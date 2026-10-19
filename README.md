# Infrastructure context system

A plain-Markdown context tree that an AI coding agent loads **selectively** before it writes
infrastructure code, so it works from your organisation's actual patterns instead of from
its training data.

> **This repository is the skeleton, not the content.** It is extracted from a system I
> built at work that documented one company's infrastructure for AI agents. The design —
> the three layers, the routing table, the authoring conventions, the per-file template —
> is reproduced in full. Every file's section structure is the real one. The bodies, which
> were that company's project IDs, hostnames, service names and CIDR blocks, have been
> replaced with a one-line statement of what belongs in each section.
>
> Fill it in for your own estate and it works. That is the point: the shape is the asset.

## The problem it solves

An AI coding agent asked to "add a Pub/Sub consumer to the billing service" will produce
something that works and looks nothing like the other forty services. It does not know your
naming convention, which Terraform module you use, that you put dead letters in GCS, or that
one region is primary and the other is DR.

A `CLAUDE.md` tells it *how to work*. It does not tell it *what the system is*. This fills
that gap, in a form an agent can load a slice of rather than all of.

## Three layers

```
L1  system-overview.md                Always loaded.         ~500-800 tokens
    │                                 System map + the routing table.
    ▼
L2  service-catalog.md                Loaded selectively.    ~1,500-7,000 tokens
    domains/*.md    ← what exists, by concern
    systems/*.md    ← deep dives on the non-standard things
    patterns/*.md   ← how things should be built
    │
    ▼
L3  <each-repo>/standards.md          Loaded in that repo.   ~300-500 tokens
    (lives in the service repo, not here; templates/standards-template.md is the skeleton)
```

The token budget is a design constraint, not an afterthought:

| Load | Roughly |
| --- | --- |
| L1 only | 500–800 |
| L1 + one domain | 1,500–2,500 |
| L1 + domain + 2-3 patterns | 4,000–6,000 |
| L1 + catalog + every domain | 5,000–7,000 |
| Everything | 8,000–10,000 |

## Five kinds of file, and the line between them

| Directory | Mode | Answers |
| --- | --- | --- |
| `domains/` | **descriptive** | "How does *X* infrastructure work across the org?" |
| `systems/` | **descriptive** | "How does *this specific system* work?" — only for things that do not follow the standard pattern |
| `patterns/` | **prescriptive** | "How should I build *this*?" — exact config, code, IaC, checklist |
| `service-catalog.md` | **lookup** | "Which project / Sentry project / Datadog service is *this* service?" |
| `templates/`, `examples/` | authoring + eval | The L3 skeleton, and a test that proves routing works |

The mapping between the descriptive and prescriptive halves is explicit:

```
 domains/ (what exists)              patterns/ (how to build it)
 data-and-storage.md        ───►     service/data-layer/sql-2022.md
 gcp-infrastructure.md      ───►     service/compute/cloud-run.md
 networking-and-security.md ───►     networking/psc.md
```

**A system file exists only where the pattern would lie.** A standard service is fully
explained by `service-catalog.md` + the relevant pattern; writing a system file for it would
duplicate the pattern and then drift from it. `systems/_index.md` carries the admission test.

Patterns split again, into **holistic** (whole-stack: `dotnet-service.md`, `ado-pipeline.md`,
`bash.md`, …) and **decomposed** (one concern each, under `patterns/service/**` and the
cross-cutting `iac/`, `networking/`, `security/`, `cicd/`). A holistic file ends by pointing
into the decomposed ones.

## How an agent actually loads it

Three entry points, all reading the same tree:

**1. Claude Code** — the user adds to their `CLAUDE.md`:

```markdown
## System Context
@system-overview.md
```

That auto-loads L1. The agent then follows L1's routing table and reads deeper files itself.

**2. A pipeline agent** — check the repo out and point the agent at it:

```yaml
- checkout: git://<your-project>/infra-context
  path: infra-context
  fetchDepth: 1
```

The agent loads `system-overview.md` into its system prompt and exposes a `load_context`
tool that reads additional files during its loop.

**3. A human** — start at `system-overview.md` and follow the links.

### The routing table is the mechanism

`system-overview.md` opens with a hard-stop instruction and a keyword → file table:

> **STOP — Load Context Before Writing Code**
> You MUST load the relevant context files below BEFORE writing any code, pipeline YAML,
> Terraform, scripts, or infrastructure configuration. Never generate infrastructure code
> from training data alone. **Multiple matches = load ALL matching files.**

Without that, agents reliably skip the context and generate plausible-looking code from
training data. The imperative tone is doing work.

## Authoring rules

| What | Rule |
| --- | --- |
| Branching | Feature branch and PR. Never push to `main`. |
| Style | Tables beat prose. Facts beat opinions. |
| Links | Relative paths, within this repo. |
| Freshness | Update `Last Reviewed` on every file you touch. |
| Tree | Add, remove or rename a file → update the tree in this README. |
| Naming | lowercase, hyphen-separated, no spaces. Index files are `_index.md`. |

**When a new file is justified:**

- **Domain** — a cross-cutting concern affecting 3+ services.
- **System** — meets 3+ of the criteria in `systems/_index.md`.
- **Pattern** — a convention reused across 3+ repos.

**The deduplication rule**, which is what keeps the hub-and-spoke from rotting: a domain
file gives the **summary** and links to the system file; the system file gives the **detail**
and links back to the domain for cross-cutting context. The same table never lives in two
places.

**Staleness:** every file carries `Last Reviewed: YYYY-MM-DD`. Anything older than 90 days
gets flagged during planning. The skeleton files here are stamped `1970-01-01` so that a
freshness check flags all of them immediately — they are empty and should be.

## The pattern file template

Every decomposed pattern uses the same sections, in this order. The consistency is what lets
an agent skim to the section it needs:

```
# <Pattern name>
## When to Use                        scope, and when it does not apply
## Standard Structure                 the canonical file/directory layout
## Configuration                      required settings, per environment
## Code Patterns                      the idiomatic implementation, as code
## Infrastructure (Terraform/Terragrunt)   the module and a worked block
## Pipeline Integration               the CI stages it needs, in order
## Local Development                  how to run it on a laptop
## Checklist                          ### New Service Setup / ### Audit Existing Service
## Related Patterns                   what it is usually composed with
## Last Reviewed: YYYY-MM-DD
```

Domain and system files have their own fixed orders; see
[`CONTRIBUTING.md`](CONTRIBUTING.md).

## Tree

```
system-overview.md          L1. Always loaded. The routing table lives here.
service-catalog.md          L2. One row per service: project, regions, deps, observability.
reference-docs.md           External vendor docs, paired with your own tenant URLs.
CONTRIBUTING.md             Authoring rules and the required section orders.
context-system-diagram.mmd  The layer model as Mermaid.

domains/                    7 files (6 + index). Descriptive, by concern.
systems/                    7 files (6 + index). Descriptive, deep dives. _index.md holds the admission test.
patterns/                   45 files. Prescriptive. _index.md routes and composes them.
  ├─ cicd/ iac/ networking/ security/     cross-cutting
  └─ service/                             per-service building blocks
       cicd/ compute/ data-layer/ docker/ messaging/ observability/ service-scaffolding/
templates/standards-template.md   The L3 skeleton a service repo fills in.
examples/                   An eval that proves routing works.
bin/e2e.py                  Checks this repo against its own conventions.
```

## Verifying

```bash
python bin/e2e.py
```

The conventions above are only real if something enforces them. This checks that every
directory with more than one file has an index, that every file carries a `Last Reviewed`
line, that pattern files use the template's section order, that every relative link
resolves, that the tree in this README matches what is on disk, and that no employer
identifiers survived the extraction. Non-zero exit on any failure.

The original system had **no tooling at all** — every rule was enforced by human PR review.
So the checker is the one thing here that is new rather than extracted, and it immediately
earned its place: on first run it found four pattern files with `Infrastructure` before
`Code Patterns`, a `domains/` directory with no index, and the README claiming a file count
that was wrong. All three are exactly the drift a convention with no enforcement produces.

## What was removed

For honesty about what this is:

- Every file body — project IDs, hostnames, DNS zones, CIDR blocks, service and database
  names, service-account emails, secret names, dashboard and on-call object IDs, wiki page
  IDs, named colleagues.
- Three unrelated scratch Python files that had been left at the root.
- Two generated example outputs (a pipeline and a PowerShell report) whose value was in the
  specific resources they queried.
- The rendered diagram PNG, since its source changed. The `.mmd` remains.

Three system files were also renamed, because the filenames themselves were product names.

## License

MIT — see [LICENSE](LICENSE).
