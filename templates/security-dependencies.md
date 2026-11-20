# Security & Dependencies

Triage relevant advisories, plan narrowly scoped fixes and track remediation into the affected environment.

## First-run questions

1. Which repos, runtimes, package ecosystems, registries and scanner results are in scope? Which updater already opens PRs?
2. What proves a deployed version, image digest or SBOM? Which deployments can you verify?
3. What severity, deadline and private reporting rules apply? Who may publish the PR or authorize an urgent production change?

## Operating steps

- Collect authoritative advisories and configured scanner alerts. Inspect manifests, lockfiles, build runtimes and deployed digests. Distinguish build, dependency and production findings. Classify applicability as affected, unaffected with evidence, or unknown. Prioritize confirmed exposure, upstream support and exploit status as reported by trusted sources.
- Deduplicate aliases such as CVE and GHSA, then group by repository, component and affected deployment. Link existing alerts or dependency PRs. Never reproduce an exploit.
- Propose the smallest viable fixed update or defensive change through the chosen spec adapter. Include compatibility, regression checks, inventory or scanner after-state and rollback. Keep sensitive findings in the authorized private channel. Draft or publish a patch only through the configured authorization and review path.
- Track source merged, artifact built, and corrected version deployed separately. Keep the case open when the affected environment cannot be verified.

Onboarding dry run: correlate one historical advisory and demonstrate the evidence needed to mark it remediated.
