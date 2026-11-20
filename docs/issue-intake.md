# Issue intake and Agile delivery

Spec & Delivery owns the intake queue. The other roles use the same work ID for review, release and closure. Pick one tracker as the authority for priority, assignment and planning state. Keep each source ticket's own state.

## Connect the sources you use

| Source | Fast signal | Reconciliation |
| --- | --- | --- |
| GitHub | `github.issue_opened` where the Orca connector delivers it | Use the approved GitHub connector or `gh api` for the selected repo. Read issue changes with `state=all` and `since`, follow every page and exclude entries with a `pull_request` field. |
| Linear | `linear.issue_created` on the confirmed team | Use `orca linear list-issues --workspace <id> --team <team> --updated-at <time> --json` on the connected host. Check truncation and cursor, and map the team's done and canceled state types explicitly. |
| GitLab | Optional configured issue webhook or approved relay | Use the authorized project Issues API (`GET /projects/:id/issues`) or an authenticated `glab` on that host. Use the exact instance and project, request changed issues with `updated_after`, and follow pagination. Re-read any webhook's issue from the trusted project before triage. |

GitLab has no native issue event in the inspected Orca v1.4.266 trigger catalog. Start with scheduled polling and only enable the optional webhook after testing its authentication and scope. GitHub and Linear events cover fast intake. The scheduled pass covers edits, closes and event gaps, including activity that Orca may suppress for the owner's own actions. Keep a last-success cursor per source. Advance it after all pages are processed and the result is saved. A missing or truncated response makes that scope partial or unavailable.

For a paused Linear routine preview, after verifying its scoped event in Orca:

```sh
python3 scripts/pack.py routine-plan .local/profile.json \
  --role spec-delivery --bot "Spec & Delivery" \
  --routine linear-issue-created --available-event linear.issue_created \
  --linear-scope ENG
```

Use the actual team key or resolved connector scope in place of `ENG`. A team shared by multiple repos also needs an owner-confirmed mapping from issues to repos. The bot must report unmatched items for triage.

## One work item can have several source tickets

Only link two records after confirming an intentional mirror, a trusted integration mapping, or the owner's decision. A reference in a ticket can mean a dependency or related work. A matching title or issue number can suggest a review. Neither changes grouping automatically.

Use a stable reference of the form `tracker:scope:id`. For GitHub or GitLab, scope identifies the approved instance and repository/project and the ID is the issue number within that project. Use a stable configured slug when a scope identifier contains a colon. For Linear, use the workspace scope and the issue UUID. Keep existing work IDs when a mirror is discovered after implementation starts. Choose a primary ref and include every mirror ref in the work record.

The [sample snapshot](../profiles/issue-intake.example.json) contains a GitHub issue and its intentional Linear mirror, both open, plus a GitLab issue with the same title. The local reconciler returns two work items and leaves all ticket states intact.

```sh
python3 scripts/issue_intake.py profiles/issue-intake.example.json
```

For recurring use, keep the normalized snapshot and mappings in owner-approved private project state. Merge incremental observations into the previously observed issue records by ref, including newly closed ones. A ticket absent from an incremental page proves nothing about its state. Keep unresolved link records even when a source is temporarily down. The helper reads a normalized snapshot and returns matches. Configured bot connectors or read-only APIs perform collection. No provider writes are performed by the helper.

## Move work through the team's process

| Stage | Bot output | Condition to move forward |
| --- | --- | --- |
| Inbox → triaged | Impact, possible mirrors, owner, next decision | Identify the work item and capture enough context to prioritize. |
| Triaged → ready | Proposed scope, dependencies, criteria and priority | Apply the team's readiness rules. In a flow board, respect WIP limits. In cycles, propose work against capacity and a cycle goal. |
| Ready → delivery | Approved spec, stable work ID and worktree | Check the configured approval signal and dispatch authorization. Reuse the existing worktree if one exists. |
| Delivery → review | Candidate SHA, test evidence, docs impact and tracker refs | Review the current candidate and preserve all criterion gaps. |
| Review → integrated → deployed | Merge or release and environment evidence | Apply the configured promotion and done rules. Propose any tracker write under the owner's policy. |
| Follow-up | Outcome, blockers, carryover and one process improvement | Use actual signals at the team's review cadence. Count a group of mirrors as one item. |

The board may use different state names. Map these stages to its existing states instead of creating new ones by default. For example, a GitHub issue can remain open for reporters while Linear tracks the team's delivery. Carry the optional `work_item` object from the [handoff example](../profiles/handoff.example.json) through the lifecycle. A closed source issue is an observation and cannot prove deployment or completion.

The scheduled refinement and delivery review recipes are optional. Set their cadence to the actual team rhythm. Use a short report for exceptions, WIP and decisions. Track cycle outcomes and flow over time when timestamps are available.

## First install check

Replay a confirmed GitHub–Linear mirror and an unrelated same-title item on GitLab. Confirm one work ID for the mirrors and the independent GitLab item. Simulate missing coverage and repeat the catch-up. Verify no duplicate spec or ticket was proposed and that the previous source status is not silently changed. Then exercise the handoff against an approved spec and an actual candidate. Test each enabled live connector on its intended host.

[Orca event catalog](https://github.com/stablyai/orca/blob/v1.4.266/src/shared/automation-event-triggers.ts) · [GitHub Issues API](https://docs.github.com/en/rest/issues/issues#list-repository-issues) · [GitLab Issues API](https://docs.gitlab.com/api/issues/)
