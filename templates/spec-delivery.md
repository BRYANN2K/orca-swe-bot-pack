# Spec & Delivery

Turn product intent into approved, verifiable changes and keep implementation attached to the right worktree.

## First-run questions

1. Which system do you use: Stipulate, OpenSpec, Markdown, or something else? Where do its change records live? Show one accepted example if the workflow is custom.
2. What exact evidence authorizes execution? For Stipulate, confirm its local version and approval state or digest. For OpenSpec, confirm the schema, installed version and team approval signal. For Markdown, confirm the approved path and immutable revision or checksum.
3. How do you name, base, and reuse worktrees? Which agent drafts the spec, which implements, and is there a concurrency limit? Which transitions require direct confirmation?

## Operating steps

- Read repository conventions and the selected spec tool's version-matched help. Map explore, validate, implement, verify and close to local commands only when present. For unsupported workflows, draft in the local format and request the owner's procedure.
- Specify user problem, scope, scenarios, constraints, acceptance criteria, data and compatibility impact, rollout and open decisions. For a product-facing change, agree on the expected user outcome, an observable signal and when to review it. Present the exact approved revision before dispatch.
- Resolve the worktree by repository and change ID before creating one. For a Stipulate repo, check the approval against the current contract and keep approved files byte-for-byte. Record execution evidence in the repo's prescribed place. Reuse the existing session where possible and reconcile uncertain launch receipts before retry.
- Send Review & Docs a handoff with candidate SHA or worktree snapshot, acceptance criteria, evidence links, and known gaps. Escalate scope changes to the owner. Never upgrade a draft or an agent completion to approval.

Onboarding dry run: pick an existing approved change and identify its worktree and approval evidence without creating a new worker.
