# Reference Class: Production Service

A team-maintained backend service, web application, API server, or long-running system serving live traffic or business-critical workloads. Outages and regressions have real consequences: customer-visible failures, pages to on-call, revenue impact, or blocked downstream teams.

## Signals That Indicate This Class

- 5+ committers in the last 12 months, or a committing org/team identity
- Deployment infrastructure is present: Dockerfile targeting runtime, Kubernetes manifests, Helm charts, Terraform, `Procfile`, systemd units, `fly.toml`, `render.yaml`, etc.
- Observability scaffolding: logging libraries wired in, metrics emission, tracing (OpenTelemetry, Datadog, New Relic, etc.)
- Environment separation: `config/production.yml`, `.env.example`, `environments/`, or equivalent
- Database migration infrastructure in commit history
- On-call rotation artifacts: runbooks, `RUNBOOK.md`, incident-response docs, alerting configs
- User's invocation lens is `inheriting work project`, `onboarding teammate`, `evaluating for acquisition`

## Counter-Signals (If Observed, Consider Another Class)

- No deployment artifacts, runs only on the author's machine → probably `solo-utility` or `prototype`
- Library consumed by many projects but not itself deployed → probably `oss-library`
- Frequent "experimental" commits, no production deploy → probably `prototype`

## Class-Relevant Strategic Concerns

- **Operational posture is first-class.** A service's health includes its observability, its deployability, and its incident-response readiness — not just its code quality.
- **Regression risk is asymmetric.** A shipped bug costs more than in other classes. Test coverage and CI gating carry more weight.
- **Multi-contributor discipline matters.** Style consistency, review practices, and documentation-for-strangers are not nice-to-haves; they are load-bearing.
- **Environment parity is a genuine concern.** Dev/staging/production configuration drift is a frequent source of incidents.

## Dimension Rubrics

### Test Health

**Foundational** — Core request-handling paths have tests. Critical business logic (payments, auth, data integrity) is exercised by automated tests. Test suite runs without production credentials.
*Signals:* tests exist for primary HTTP handlers or RPC endpoints; `tests/` or equivalent has meaningful content; test run succeeds on a clean checkout.

**Adequate** — Unit and integration tests cover the primary request-handling paths and the documented business rules. Failure paths are tested. Coverage is measured and visible.
*Signals:* coverage report produced by CI; line coverage ≥ ~60% for core modules; integration tests exercise at least happy-path HTTP/RPC flows against a test instance of dependencies.

**Strong** — Comprehensive unit, integration, and at least some end-to-end tests. Tests exercise failure modes (timeouts, malformed input, dependency failures). New features customarily ship with tests. Flake rate is tracked and addressed.
*Signals:* coverage ≥ ~80% for core modules; integration suite includes DB/cache/external-service fakes or containers; test suite runs in CI in bounded time.

### Dependency Health

**Foundational** — Dependencies are pinned (lockfile present and committed). The service can be built reproducibly. No known-critical CVEs in directly reachable code paths.
*Signals:* lockfile present (`package-lock.json`, `Gemfile.lock`, `poetry.lock`, `go.sum`); audit tool shows no critical/high severity unfixed findings.

**Adequate** — Dependencies are actively managed. Security updates are applied within weeks, not years. The service is not accumulating technical debt from abandoned packages.
*Signals:* commit log shows dep bumps in the last 90 days; `npm audit` / `bundle audit` / equivalent shows only low-severity findings or clean; <20% of direct deps more than one major version behind.

**Strong** — Dependencies are part of the team's operational practice. A documented upgrade cadence exists. Tools like Dependabot, Renovate, or equivalent are configured and acted on.
*Signals:* Dependabot/Renovate config present; PRs from automated dep-bump tools are merged or addressed on a visible cadence; dependency surface is intentional (no bloat from unused transitive deps).

### CI / Automation Health

For this class, CI is mandatory at the Foundational level. A production service without CI is a Safety finding.

**Foundational** — CI runs on every push and PR, gates merges on test passage, and publishes build artifacts or images.
*Signals:* `.github/workflows/`, `.gitea/workflows/`, `.gitlab-ci.yml`, or equivalent present; recent runs succeed; CI status is visible on PRs.

**Adequate** — CI enforces multiple quality gates: tests, lint, type-check (where applicable), security audit. Deployment automation exists and is used (push-button or GitOps-style).
*Signals:* multiple job types in CI config; deployment workflow or deployment docs present; release process is documented and reproducible.

**Strong** — CI gates are comprehensive and fast. Canary or staged deployment is possible. CI is treated as production infrastructure: flakes are diagnosed, broken pipelines are priority-1.
*Signals:* CI includes integration tests against ephemeral dependencies; deployment includes pre-deploy verification (smoke tests, canary analysis); CI run time is bounded and stable.

### Documentation

**Foundational** — A README explains what the service is, its public surface (endpoints, protocols), and how to run it locally. A new team member can get the service running in a reasonable time.
*Signals:* `README.md` covers service purpose, local-run instructions, and primary endpoints; `.env.example` or equivalent lists required configuration.

**Adequate** — Operational documentation exists: runbooks for common incidents, deployment procedures, environment differences, and on-call guidance. Business logic that's non-obvious is documented near the code.
*Signals:* `RUNBOOK.md`, `docs/operations/`, `OPERATIONS.md`, or equivalent present; deployment procedure documented; alerting and on-call docs visible.

**Strong** — Documentation supports both engineering and operations at stranger-onboarding quality. Architecture docs exist. Decision records (ADRs) capture why the system is structured as it is. Incidents produce postmortem docs that feed back into runbooks.
*Signals:* `docs/`, `architecture/`, or ADR directory present; postmortem or incident-review artifacts visible; runbooks are current (recent updates).

### Architecture Hygiene

**Foundational** — The service's structure is legible. A new engineer can locate the entry point, the request-handling layer, and the data layer within an hour. Business logic is not splattered across presentation code.
*Signals:* conventional framework layout (MVC, hexagonal, or the framework's idiomatic pattern); clear separation of HTTP/routing layer from business logic; data access is not duplicated across files.

**Adequate** — Responsibilities are modular. Cross-cutting concerns (auth, logging, error handling) are centralized, not ad-hoc. External dependencies (database, cache, queue) are abstracted behind clear seams.
*Signals:* consistent auth/error/logging patterns across handlers; clear repository/service/controller separation or equivalent; dependency-injection or factory patterns for external services.

**Strong** — The architecture is deliberately designed for the team's ownership model. Deployment units match ownership boundaries. Change paths are predictable (a new feature touches a predictable set of files). Technical debt is acknowledged, tracked, and amortized.
*Signals:* module-level ownership is discoverable (CODEOWNERS, directory-level README); cross-module coupling is intentional and documented; visible effort on managing technical debt (commits tagged as refactor, debt-reduction PRs).
