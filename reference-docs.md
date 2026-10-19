# Reference docs

> **Skeleton.** External vendor documentation, each paired with **your own** tenant or
> instance URL. The pairing is the point: an agent that knows the vendor's docs still does
> not know which region, org or workspace you are on, and will confidently guess wrong.

## Links

| Vendor | What it covers | Vendor docs | Your instance |
| --- | --- | --- | --- |
| `<observability>` | metrics, monitors, dashboards, APM | `<docs URL>` | `<your org URL / site region>` |
| `<error tracking>` | issues, releases, source maps | `<docs URL>` | `<your org URL>` |
| `<cloud provider>` | the services you actually use | `<docs URL>` | `<console URL, org id>` |
| `<deployment tool>` | projects, releases, runbooks | `<docs URL>` | `<your instance URL>` |
| `<on-call>` | services, escalation, event rules | `<docs URL>` | `<your subdomain>` |
| `<MCP gateway>` | which tool servers an agent can reach | `<docs URL>` | `<your gateway URL>` |

## Notes

<!--
Anything an agent gets wrong about a vendor by default. For example: which API version your
org is pinned to, a region-specific hostname, an endpoint whose documented default is wrong
for your setup, a parameter the server silently ignores. One line each, dated.
-->

## Last Reviewed: 1970-01-01
