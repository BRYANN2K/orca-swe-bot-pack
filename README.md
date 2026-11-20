<div align="center">

<img src="assets/banner.png" alt="Orca SWE Bot Pack. Three pixel-art bots represent delivery, review and maintenance, and release and operations." width="100%">

**Three bot templates for software and product engineers working with AI agents.**

Start with one job. Each bot learns your repo, your workflow, and what it can do before you turn on its routines.

[Quick start](#quick-start) · [Browse the bots](#the-three-bots) · [Issue intake & Agile delivery](docs/issue-intake.md) · [Orca import and sharing](docs/orca-import.md)

</div>

---

## Why this pack?

Between a spec and a release, there is work that repeats. Someone has to find the approved contract, check the PR against it, update the docs, reuse the right worktree, and verify what actually shipped. The templates give those jobs a consistent home in Orca.

- **Bring your own workflow.** Start with [Stipulate](https://github.com/BRYANN2K/stipulate-skills), OpenSpec, Markdown specs, or your team's process. Each bot asks about the branches, CI, environments and approval signals it needs for its role.
- **Start with delivery and review.** Give both bots the same confirmed project profile. Add Release & Operations when you need deployment or infrastructure follow-up.
- **Review routines before they run.** Choose the scope and destination, try a historical case, and create selected routines paused. Set permissions separately for worker dispatch, PR publication, cleanup and deployment.

**Status.** The three native Orca shares, six standalone modules, and local preflight are available. A full recipient-side import and live delivery of automation events still need an Orca test.

## Quick start

You need Orca with Bots enabled and an agent available on the chosen host. Python 3.10+ is required for the optional local preflight commands.

In Orca, open **Bots → + → New bot → Start from a template → From a link**. Paste one of the links below, review the contents, and choose the host, agent, and permissions. Use the setup note to start the interview. Starter automations arrive paused.

### Install from Git

From the parent directory where you keep projects, clone the pack and add it to Orca. The private repository requires GitHub SSH access on that host.

```sh
git clone git@github.com:BRYANN2K/orca-swe-bot-pack.git && orca repo add --path "$PWD/orca-swe-bot-pack"
```

This adds the Git project to Orca. Continue with the role you want to install.

1. Pick a role from [the three bots](#the-three-bots). Create a bot in Orca and choose its host, agent and approval mode.
2. Paste the role's Markdown into its chat. Add this instruction and give it the repo and host when you know them.

   ```text
   Run this template's setup interview. Show me what you detect before saving
   a profile or adding automations.
   ```

3. Review the answers and confirm the profile. Have the bot try a historical PR or change in read-only mode. Open a new chat and verify that it recovers the role and repo scope.
4. Use the [preflight guide](docs/preflight.md) to preview the routines you want. Approve their creation paused, check the saved scopes and destinations, then enable the ones you want to run.

Sample profiles for [Stipulate](profiles/stipulate.json), [OpenSpec](profiles/openspec.json) and [Markdown + main](profiles/markdown-main.json) show which fields to confirm for a real repository.

## The three bots

| Bot | Capabilities | Orca |
| --- | --- | --- |
| [Spec & Delivery](dist/spec-delivery.md) | Triage issues from GitHub, GitLab or Linear and turn one ready work item into an approved spec. | [Import Spec & Delivery](https://share.onorca.dev/bots/share/a3e4b58b003b4f488f77b72aea395267) |
| [Review & Maintenance](dist/review-maintenance.md) | Independent PR and docs review, repository and worktree maintenance, and security and dependency triage. | [Import Review & Maintenance](https://share.onorca.dev/bots/share/a09dc9edd8d44ef2b659856fb274d151) |
| [Release & Operations](dist/release-operations.md) | Optional bot for environment promotions, release notes, rollback, and infrastructure health. | [Import Release & Operations](https://share.onorca.dev/bots/share/0995ad64efdd4c518e750e458a4eca71) |

Enable modules one at a time within each bot. The original prompts also work as standalone modules.

- **Spec & Delivery** · [Spec & Delivery module](dist/spec-delivery.md)
- **Review & Maintenance** · [PR Review & Docs](dist/pr-review-docs.md), [Repository Maintenance](dist/repo-maintenance.md), [Security & Dependencies](dist/security-dependencies.md)
- **Release & Operations** · [Release & Environments](dist/release-environments.md), [Infrastructure Operations](dist/infrastructure-operations.md)

## How the bots work together

On a project that uses one worktree per spec, a feature can move through the pack like this.

1. **Triage and plan.** Spec & Delivery detects new work in the configured trackers. A confirmed GitHub–Linear mirror can stay open in both. The team plans one work item within its cycle capacity or WIP limit.
2. **Agree on scope.** Spec & Delivery records the approved revision, dispatches the worker when authorized, and reuses the same worktree for corrections.
3. **Review the candidate.** Review & Maintenance checks the exact commit independently and sends any fixes back to the delivery worker in the same PR.
4. **Ship, close and learn.** Release & Operations ties evidence to the promoted candidate. Review & Maintenance checks the merged worktree before any authorized cleanup. Delivery follows up on the product outcome and flow at the team's agreed cadence.

Security and infra changes can enter the same flow. An advisory or a GitOps discrepancy starts with evidence and a proposed change. The worker takes it through the configured approval, PR and release steps. Each role can also return its result directly in chat when installed on its own.

[Automation recipes and catch-up behavior](docs/automations.md) · [Shared handoff example](profiles/handoff.example.json)

## Share templates through Orca

Each native share includes the role, its setup note, its skills, and its paused starter schedules. The [import guide](docs/orca-import.md) documents how to rebuild a share and which connector and event settings recipients supply.

## Develop and verify

Open a pull request into `main` for changes to the pack.

Edit the source role in `templates/` and regenerate the standalone file in `dist/`. These commands run locally.

```sh
python3 scripts/build.py
python3 scripts/build.py --check
python3 -m unittest discover -s scripts
```

The [preflight guide](docs/preflight.md) also covers the profile checker, handoff validation, routine previews, and the pilot acceptance checks.
