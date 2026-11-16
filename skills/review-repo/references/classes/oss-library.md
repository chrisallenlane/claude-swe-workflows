# Reference Class: OSS Library with External Consumers

A library, SDK, or package published to a public registry (npm, PyPI, crates.io, Maven Central, pkg.go.dev, etc.) and consumed by third-party projects the authors do not control. The primary obligation is a stable, well-documented contract that strangers can depend on.

## Signals That Indicate This Class

- Package manifest declares publishability: `"private": false` in `package.json`, `setup.py` / `pyproject.toml` with publishable metadata, `Cargo.toml` with `[package]` metadata, `go.mod` module path matching an importable location
- Published tags / semver releases visible in git: `v1.0.0`, `v2.3.1`, etc. (not just `main`)
- `CHANGELOG.md` or release notes present
- External issues or PRs in history (inbound contributions from outside the core committers)
- Documentation is written for strangers ("Installation," "Getting Started," "API Reference")
- User's invocation lens is `evaluating foss` or `maintaining shared library`

## Counter-Signals (If Observed, Consider Another Class)

- No published package, no registry presence → probably `solo-utility`
- The library is deployed as a service → probably `production-service`
- No semver discipline, no CHANGELOG, frequent breaking changes → probably `prototype` (even if published)

## Class-Relevant Strategic Concerns

- **API stability is non-negotiable.** Consumers cannot be asked to re-integrate on the author's whim. Breaking changes demand major-version bumps and clear migration paths.
- **Documentation is consumed by strangers.** Quality of API reference, usage examples, and contract description is load-bearing.
- **Semver discipline is a capability signal.** A library that breaks consumers on patch bumps is failing a baseline competence check.
- **Contribution experience matters.** External contributors need to be able to get productive without insider knowledge.
- **Supply chain posture is relevant.** The library's dependencies become its consumers' transitive deps; staleness and security posture propagate.

## Dimension Rubrics

### Test Health

**Foundational** — The public API surface is tested. A consumer can trust that documented behavior is verified behavior. No major documented feature is entirely untested.
*Signals:* tests exist for exported/public symbols; test suite exercises the library's advertised usage examples; test run succeeds on a clean clone.

**Adequate** — Tests cover the public API comprehensively, including documented edge cases and error conditions. Tests run across the library's supported runtime versions. Coverage is published.
*Signals:* coverage ≥ ~75% for public API modules; tests run against a version matrix (e.g., Python 3.8-3.12, Node 18-22); coverage badge or report visible.

**Strong** — Comprehensive test suite including property-based tests, fuzz tests where applicable, and tests of the library's integration with common consumer patterns. Backward-compatibility is explicitly tested across releases.
*Signals:* property-based tests (`hypothesis`, `fast-check`, `quickcheck`, etc.) present; contract tests exist; test suite includes backward-compat verification or regression-test corpus.

### Dependency Health

**Foundational** — Dependencies are minimal and pinned appropriately for a library (loose pins in the manifest; lockfile for development). No known-abandoned packages. No transitive CVEs in reachable code paths.
*Signals:* `dependencies` in manifest is small; no unused deps; `npm audit` / `pip-audit` shows no high-severity findings in reachable paths.

**Adequate** — Dependencies are intentionally chosen. The library minimizes impact on consumers: permissive version ranges where safe, no heavy transitive pulls, no deps with known license incompatibilities.
*Signals:* direct deps are well-maintained and widely-adopted; license compatibility is clean (no GPL in an MIT library without explicit handling); dep upgrade commits visible in history.

**Strong** — Dependency surface is deliberately minimal. The library's inclusion cost to consumers is consciously managed. A documented policy on deps exists (e.g., "no new runtime deps without justification").
*Signals:* `dependencies` count is small relative to library scope; `peerDependencies` used where appropriate; CONTRIBUTING or similar documents dep policy.

### CI / Automation Health

**Foundational** — CI runs tests on every push and PR. Published releases are cut from CI-verified artifacts, not from a maintainer's laptop.
*Signals:* CI workflow present and green on recent runs; release workflow or tag-triggered publishing configured.

**Adequate** — CI tests across the library's supported runtime versions and platforms. Lint and type-check gates are enforced. Release automation is reproducible.
*Signals:* test matrix across language/runtime versions; lint and type-check jobs present; release workflow publishes from a tag with provenance.

**Strong** — CI includes comprehensive quality gates: tests (matrix), lint, type-check, security audit, docs build, backward-compat checks. Release process includes provenance (SLSA, signed commits/tags, or similar).
*Signals:* full CI matrix; docs build verified in CI; signed tags or SLSA provenance; release-blocking checks are comprehensive.

### Documentation

**Foundational** — README covers installation, basic usage, and a pointer to the full API reference. A first-time user can install the library and use its primary feature.
*Signals:* README has install instructions, at least one runnable usage example, and a pointer to API docs; package registry page renders README correctly.

**Adequate** — API reference exists and is kept current. Common patterns and recipes are documented. Migration guides accompany major-version releases. A CHANGELOG tracks user-visible changes.
*Signals:* generated or curated API reference present (`docs/`, `docs/api.md`, Sphinx, JSDoc, etc.); CHANGELOG.md with meaningful entries; migration notes or UPGRADING docs for major versions.

**Strong** — Documentation supports both discovery and mastery. Tutorials, conceptual guides, recipes, and comprehensive API reference all exist. Examples are tested as part of CI. External contributor documentation is robust.
*Signals:* documentation site with multiple genres (tutorial, how-to, reference, explanation — the Diátaxis pattern or similar); doctest or example verification in CI; CONTRIBUTING.md, CODE_OF_CONDUCT.md, and issue/PR templates present.

### Architecture Hygiene

**Foundational** — The library's public surface is clear. A consumer can distinguish public API from internal implementation. Exports are intentional, not accidental.
*Signals:* explicit `__init__.py` with `__all__`, `index.ts` / `index.js` with explicit exports, `pub` marked intentionally in Rust, capitalized exports in Go; no accidental exports of internals.

**Adequate** — Internal architecture is layered clearly. Breaking changes to internals don't leak to the public API. Extension points are deliberate (or deliberately absent).
*Signals:* internal modules are not accessible via documented entry points; there's a consistent pattern for what is and isn't public; plugin or extension mechanisms (where present) are documented.

**Strong** — The library's architecture supports its consumers' likely evolution. Deprecations are handled gracefully (warnings, migration paths, sunset schedules). The public API is small relative to the functionality delivered.
*Signals:* deprecation machinery present and used; public API surface is deliberately constrained; architectural decisions are documented (ADRs, design docs, or comparable).
