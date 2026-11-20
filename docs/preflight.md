# Prepare the first install

This procedure works for one role and scales to a group. Keep the Git repository, workflow tool and CI as the sources of truth. The pack's local helper reads records and prints plans. It never calls Orca or applies a plan.

## 1. Establish the project profile

Name a real repository and host. Read the repo instructions and locate an existing spec, integration branch, CI run and deployment signal. Choose the [starting profile](../profiles/stipulate.json) closest to the observed workflow. Confirm its unresolved fields with the owner. For a workflow with no CI, record the agreed manual verification provider and the required checks.

Save the confirmed JSON at an owner-approved path that the bots can read. For private local operation you can use this checkout's ignored `.local/` directory. For bots on multiple hosts, supply the same profile via an existing authenticated tracker or copy it to the hosts. A local path alone is reachable only on its host. Keep credentials outside the profile.

```sh
python3 scripts/pack.py profile-check .local/profile.json
```

The checker validates required fields, IANA timezone, explicit per-action modes and paused/private automation defaults. It cannot verify GitHub access, actual CI, or human approval. The profile can use `report` for a report only, `ask` for a separately approved action, or `manual` for owner execution.

## 2. Install and reconnect

Use the [Markdown path](../README.md#quick-start) or a reviewed [Share Bot link](orca-import.md). Keep the template role instructions in the bot's persistent setup, for example its `SOUL.md` after owner review. Keep the project profile separate. After confirming the profile, ask the bot to use one historical PR or change in read-only mode. Open a new chat and verify that it loads the same role, repo and permissions. Connect one additional role and confirm it asks only role-specific questions and unresolved shared fields.

## 3. Preview the first routine

List the selected bot's existing routines. Keep every exact name that matches a pack routine. Check `orca automations trigger-options --bot <bot> --json` on the intended host for event routines. Then preview only the routine you want. Pass each existing exact name with `--existing-name` and each verified event with `--available-event`.

```sh
python3 scripts/pack.py routine-plan .local/profile.json \
  --role pr-review-docs --bot "PR Review & Docs" --routine review-catchup
```

Review the generated plan and actual saved scope. `review-existing` means inspect the current entry rather than duplicating it. Gather existing names immediately before creating a job. A matching name is a review signal, not proof that the live settings match. After reviewing and confirming creation, add the proposed job paused and run a read-only trial. Check bot, host, scope, destination, schedule, and next execution before enabling it. Webhooks are configured manually on the recipient's host.

## 4. Verify handoffs before retrying or closing

Use the [handoff shape](../profiles/handoff.example.json). Keep a single record per repo and change in the tool the project already uses. The holder of the current task updates it and links evidence rather than overwriting other roles' conclusions. Use the same identifier when a worker, event or catch-up points at the same change. Read current state before retrying an operation with an unknown outcome.

```sh
python3 scripts/pack.py handoff-check .local/profile.json .local/handoff.json \
  --current-head "$CURRENT_HEAD" --current-contract "$CURRENT_CONTRACT"
```

Supply the observed current PR head or clean worktree commit and the current approved contract ref. Dirty worktree evidence needs the workflow tool's own snapshot. A valid handoff may still list failed or unverified criteria. Verify completeness against the original spec, check evidence freshness and use the workspace's workflow tool before advancing the lifecycle.

## Pilot acceptance

| Scenario | Result to record |
| --- | --- |
| Install one role on a clean profile and reopen its chat | The persistent role and confirmed scope are recovered. |
| Install another role for that repo | It reuses the agreed profile and asks only about missing role-specific fields. |
| Review a historical PR with a documentation change | The bot names the affected page and what must change, with a link to the candidate. |
| Change the PR head or contract after review | The old handoff is stale and a fresh review is requested. |
| Deliver the same merge event plus scheduled catch-up | The same cleanup candidate is produced once. The worktree is rechecked before any authorized removal. |
| Give the cleanup bot a merged worktree with ignored local data | It reports why it retained the worktree. |
| Disable the connector before running catch-up | The bot reports missing data and retains the last-success cursor. |
| Repeat setup with an existing routine | The plan requests review instead of proposing a duplicate creation. |
| Replay linked, open GitHub and Linear issues alongside a same-title GitLab issue | The mirrors share one work ID and retain independent states. The GitLab item remains separate. |

Run the first pass on a Stipulate repo, then use an independent OpenSpec or Markdown fixture. Log observed bot behavior, commands, and evidence separately from remaining gaps. The runtime pilot is separate from the local checks in this repository.

[Configure tracker intake and board cadence](issue-intake.md)
