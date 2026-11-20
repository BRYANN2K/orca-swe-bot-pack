# Release & Environments

Prepare auditable releases, promotions and verification on the environments the project actually uses.

## First-run questions

1. Do you use promotion branches, tags, trunk-based delivery, GitOps or release channels? Name the exact sources and targets for each transition.
2. Is the same artifact promoted, or rebuilt? How do you identify it? What proves it actually reached each environment?
3. What qualifies a release for approval? Who controls production, migration windows, rollback and public release notes?

## Operating steps

- Identify the lot by repository, source and target revisions, merge range or relevant tags, and artifact identities. Link included specs, PRs and test evidence. Surface bundled changes and migration dependencies.
- Check the configured CI and smoke tests for the same candidate. When rebuilding changes the identity, verify equivalence using the project's provenance or rerun required validation. If no staging exists, use the agreed evidence for that release channel.
- Present ready or blocked with exact missing checks. Provide rollback scope and forward-recovery constraints. Ask for required approvals. Reconcile actual post-deploy health and artifact identity. Draft release notes from the promoted range. For product-facing changes, follow up on the agreed outcome signal at the planned time and link observed results back to the change.

Onboarding dry run: prepare a dossier for a historic candidate and show that an unverified artifact blocks readiness.
