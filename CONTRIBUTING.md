# Contributing

## Quick reference

| What | Rule |
| --- | --- |
| Branch strategy | Feature branch and PR to `main`. Never push directly. |
| Content style | Tables beat prose. Facts beat opinions. |
| Cross-references | Relative paths, within this repo. |
| Last Reviewed | Update the date on every file you modify. |
| README sync | Add, remove or rename a file → update the tree in `README.md`. |
| Filenames | lowercase, hyphen-separated, no spaces. Index files are prefixed `_`. |

## When to create a new file

- **Domain** — a new cross-cutting infrastructure concern affecting 3+ services.
- **System** — meets 3+ of the criteria in [`systems/_index.md`](systems/_index.md).
- **Pattern** — a reusable convention shared across 3+ repos.

Below those thresholds, add a section to an existing file. A thin file costs more than it
saves: it is one more thing to keep fresh and one more place for the same table to drift.

## Required section order

These are fixed so an agent can skim to the section it needs without reading the file.

**Domain files**

1. `# <Domain name>`
2. `## Overview` — one or two paragraphs
3. `## Current State` — tables and structured data, `###` per sub-area
4. `## Patterns & Conventions` — a numbered list
5. `## Known Gaps / Tech Debt`
6. `## Related Context` — bulleted relative links
7. `## Wiki References` — table: Page / Topic / Link
8. `## Last Reviewed: YYYY-MM-DD`

**System files**

1. `# <System name>`
2. `## Overview` — what it is, how to reach it
3. `## Architecture`
4. `## <Cloud> Projects`
5. `## Pipeline Workflow`
6. *(system-specific sections)*
7. `## Known Gaps`
8. `## Related Context`
9. `## Wiki References`
10. `## Last Reviewed: YYYY-MM-DD`

**Pattern files**

1. `# <Pattern name>`
2. `## When to Use` — scope and applicability
3. `## Standard Structure`
4. `## Configuration`
5. `## Code Patterns`
6. `## Infrastructure (Terraform/Terragrunt)`
7. `## Pipeline Integration`
8. `## Local Development`
9. `## Checklist` — with `### New Service Setup` and `### Audit Existing Service`
10. `## Related Patterns`
11. `## Last Reviewed: YYYY-MM-DD`

A holistic pattern (one that covers a whole stack rather than one building block) may use
its own middle sections, but keeps `When to Use` first and `Last Reviewed` last, and ends
with links into the decomposed patterns it supersedes.

## The deduplication rule

This is the one that keeps the tree from rotting.

- A **domain** file gives a **summary** of a cross-cutting concern and links to the system
  file for detail.
- A **system** file gives the **full detail** and links back to the domain for the
  cross-cutting context.
- **The same table never lives in two places.** When you find yourself copying one, link
  instead and delete the copy.

## Review process

1. Branch.
2. Make the change.
3. Update `Last Reviewed` on every file you modified.
4. Verify cross-references still resolve — check the `Related Context` links.
5. Update the tree in `README.md` if the file set changed.
6. `python bin/e2e.py` — it checks 3, 4 and 5 mechanically.
7. Open the PR.

## Writing for an agent, not for a person

The consumer is an LLM with a token budget, which changes what good looks like:

- **A table beats a paragraph.** It survives truncation and is easier to extract from.
- **State the convention, then show it.** "Buckets are `<app>-<env>-<purpose>-<region>`"
  followed by one real example beats three paragraphs of explanation.
- **Say what *not* to do, explicitly.** An agent will not infer a prohibition from silence.
- **Keep one file to one concern.** Selective loading only works if the slices are clean.
- **Date every fact that can go stale.** An undated claim is indistinguishable from a
  current one, and that is how an agent confidently writes last year's config.
