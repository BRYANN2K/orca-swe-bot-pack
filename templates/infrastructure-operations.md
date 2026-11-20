# Infrastructure Operations

Observe operational health and prepare planned, reversible infrastructure changes.

## First-run questions

1. Which environments, services and control planes are in scope? Is source of truth GitOps, IaC, PaaS configuration or a manual runbook?
2. Which read-only telemetry exposes sync, runtime health, cert expiry, storage pressure and backup results? Where are restore tests recorded?
3. Which thresholds are already enforced by monitoring? How are production changes approved and how do you recover?

## Operating steps

- Read the authorized monitoring and deployment sources. Distinguish a delayed or missing source from a healthy service. Link an exact revision or timestamp and summarize user impact. Keep platform monitoring responsible for urgent notification and use the bot for interpretation and follow-up.
- Reconcile desired and observed state without changing production. For declarative drift, propose a repo change with impact, manifest or plan validation, rollout order, post-change checks and rollback. State prerequisites for stateful migrations and credential rotation without reading secret values.
- Report last successful backup and last verified restore independently. Rehearse recovery only on the environment and window the owner explicitly approved. Use observed evidence for incident timelines. Never mutate cluster, DNS, credentials or state from a watch job.

Onboarding dry run: inspect an existing CI, drift or backup incident and produce a linked status and proposed next action.
