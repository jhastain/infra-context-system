# Systems

> **Skeleton.** Deep dives on systems that do **not** follow the standard service pattern.
> This index exists mainly to hold the admission test, because the failure mode of a tree
> like this is a system file per service, each half-duplicating the pattern.

## When a system earns a file

A system qualifies on **3 or more** of:

1. It has its own cloud project or projects.
2. It has dedicated pipelines (3 or more).
3. It spans multiple infrastructure concerns — compute *and* data *and* networking.
4. It has unusual lifecycle management (ephemeral, scheduled teardown, manual promotion).
5. It does not follow the standard microservice pattern.
6. More than one person has asked "how does this actually work?"

**Standard services do not go here.** They are a row in
[`service-catalog.md`](../service-catalog.md) plus the pattern that explains them — the
pattern is the explanation, and copying it into a per-service file guarantees the copy
drifts.

## Systems

| System | Why it needs a file | Key infrastructure |
| --- | --- | --- |
| [Content archive](content-archive.md) | `<which criteria it meets>` | `<key infra>` |
| [Build infrastructure](build-infrastructure.md) | `<...>` | `<...>` |
| [Core monolith](core-monolith.md) | `<...>` | `<...>` |
| [Ephemeral environments](ephemeral-environments.md) | `<...>` | `<...>` |
| [Internal AI agent](internal-ai-agent.md) | `<...>` | `<...>` |
| [Media service](media-service.md) | `<...>` | `<...>` |

## Last Reviewed: 1970-01-01
