---
name: merged-worktree-check
description: Check whether a merged worktree can be removed without losing local work.
---

Verify that the repository host records the PR or MR as merged and the merge is on the intended target. Inspect the worktree's head, tracked changes, untracked and ignored data, stashes, and active processes. Retain uncertain candidates and record why. Recheck immediately before an explicitly authorized removal. Recommend cleanup in the report when execution is outside scope.
