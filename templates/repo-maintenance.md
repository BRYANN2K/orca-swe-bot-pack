# Repository Maintenance

Keep repositories and Orca worktrees easy to resume, review and close.

## First-run questions

1. Which clones and Orca hosts are in scope? Which integration branches and merge methods prove a change landed?
2. Which directories, data and sessions must be preserved? How do you handle stashes and local commits?
3. What age or grace period do you want? Do you want a candidate list, approved batches, or policy-based cleanup?
4. Who already owns dependency updates and CI alerts? Which routine is responsible for each signal?

## Operating steps

- Trace the merged PR to the correct target. For squash or rebase, use the PR's merge record and ancestry of the integrated result on the target. Match the local worktree HEAD to the reviewed source or independently reconcile differences.
- Inspect tracked, untracked and ignored files, unique commits, stashes, attached sessions and running services. Retain ambiguous worktrees and report the reason. Never stop active work or force remove a worktree. Recheck at deletion time. If authorized, remove through the matching Orca host and verify disappearance, then report actual disk change if measured.
- Flag finished agent changes lacking a PR for owner-directed resume or closure. Track recurring CI failures by check and normalized symptom. Propose small compatibility upgrades through delivery and reuse existing bot PRs.

Onboarding dry run: show why one merged worktree qualifies and another with private data does not.
