# PR Review & Docs

Review a candidate against its approved behavior and keep documentation synchronized with the change.

## First-run questions

1. Which checks, acceptance evidence and review sign-off are required? Do you require an independent reviewer or a particular model?
2. Where do user docs, API/MCP contracts, configuration references, examples and runbooks live? Which updates belong in the same PR?
3. Where should findings go? May the bot answer on the PR or only draft feedback in chat?

## Operating steps

- Review the requested immutable candidate and the current base. Record repository, PR number, head SHA and approved contract ref. Rerun affected checks after the head changes.
- Keep the work ID and primary and mirrored tracker refs when supplied. Report review evidence against that work item so mirrors do not start separate reviews. Hand back review or rework status without changing source issue states unless the owner configured that tracker action.
- List findings by impact with file and line, expected behavior and evidence. Classify each criterion passed, failed or unverified. Follow the repository's exact check protocol and reopen verification when evidence becomes stale.
- Compare code, screenshots, CLI text, API/MCP contracts, configuration and operational behavior with their documentation. Give affected pages and specific edits or a reasoned no-impact result. Hand corrections back to the existing implementation worktree. Do not author an approval on the owner's behalf.
- Post-merge, reconcile changed docs against shipped behavior and propose a follow-up only for gaps that still exist.

Onboarding dry run: produce a review and doc impact report for a historical PR with zero writes.
