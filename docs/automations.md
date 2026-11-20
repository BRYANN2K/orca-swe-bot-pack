# Automation design

One owner per recurring signal. The default is a private bot chat, an owner-selected IANA timezone, and no enabled jobs. Start with recommended schedules only if they replace an actual manual check. Event rules and opt-in schedules start after a dry run. A narrow event can replace its polling job if delivery is reliable and a periodic reconciliation remains available.

| Routine | Suggested local time or trigger | Output |
| --- | --- | --- |
| Security advisory catch-up | Daily 08:20 plus security alert events when supported | New relevant or unknown findings. Prioritize explicit urgent evidence. |
| Infrastructure health | Daily 08:50 plus optional scoped monitoring webhook | Changed health, stale signals, deployment mismatches, backup gaps. Monitoring handles paging. |
| Review queue | Weekdays 09:40, explicit handoff first | A changed head SHA with no current completed review. |
| Release readiness | Weekdays 10:05 during active release work | Changed state or a decision needed. Prefer deploy events for verification. |
| Delivery blockers | Weekdays 10:15, opt-in | Approved work blocked by a missing decision, quota or evidence. |
| Documentation drift | Wednesday 11:20 | Unresolved discrepancies between merged code and docs. |
| Maintenance digest | Friday 15:30 | Cleanup candidates, orphaned work, recurring CI and ordinary upgrades. |
| Restore readiness | First day of month 10:35, opt-in | Last restore evidence and any drill to schedule. |

Set timezone explicitly on each scheduled job. Choose off-peak times for shared CI and avoid overlapping expensive runs on the same host. Query `orca automations trigger-options --bot <name> --json` before saving event rules. Some events depend on Orca Cloud and a connected app. Use explicit scope and `--results-to chat` because certain event rules default to posting in the source thread. The source host must be online. Run scheduled catch-up against the configured sources for events missed during downtime. Keep a known append-only source or last-success cursor in user-controlled state when the host supports it.

A fresh run reduces accumulated context, but its useful state must live outside chat. Suggested dedupe keys are repository/PR/head for review, repo/PR/merge SHA for cleanup, repo/head/check/signature for CI, advisory/component/environment for security, deployment identity for release and monitor incident ID for infra. Include the repo and scope in the job name if one bot covers several. Never interpret a failed fetch as no findings. Retry transient failures on the next scheduled catch-up or manually. Use a bounded overlap over the last complete result and advance only once all pages are reconciled. A proposed cleanup is evidence for review. Its eligibility checks run again immediately before any authorized removal.

GitHub's `pr_opened` may skip actions by the owner and PRs made by bot workers. Dispatch a review handoff explicitly or reconcile the open queue. Treat CI and deploy event bodies as hints, then read the matching provider run. A periodic job is for reconciliation. Approval, publication, deletion and production actions require separate authority and current evidence. Avoid public posting and new worktree creation from a polling cycle.

Orca's CLI supports five-field cron, presets or RRULE, a timezone, paused creation, optional model override on a fresh bot run, event filtering, and one-shot event waits with an optional deadline. A deadline wake is not a confirmed event. Scheduled prechecks are optional, run shell commands and are bypassed by Run now. Prefer native run history and source queries to a new precheck. If one is introduced later, audit the command and design the main prompt to check its own prerequisites too.

Example for a paused scheduled routine after owner approval:

```sh
orca automations create --bot "Security & Dependencies" \
  --name "SWE Pack · security-catchup · example/app" \
  --trigger "20 8 * * *" --timezone "Europe/Brussels" \
  --runs-in new --results-to chat --disabled \
  --prompt "Reconcile configured advisory sources for example/app using the confirmed profile. Report newly affected or unknown components in chat." --json
```

After creation, inspect the saved host, scope, schedule, next run and destination. Test read-only first. Use support for a single owner digest only when a bot actually has access to the other results or a shared approved tracker. The individual templates work without a digest coordinator.

[Versioned Orca automation guide](https://github.com/stablyai/orca/blob/v1.4.266/skill-guides/orca-cli/references/automations.md)
