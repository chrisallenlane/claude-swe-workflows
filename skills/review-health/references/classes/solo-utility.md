# Reference Class: Solo or Small-Team Utility

A CLI tool, internal utility, automation script, or single-purpose helper maintained by one person or a small team (<5 active contributors). The project's primary audience is its authors plus a small, known user base. Reliability matters, but the failure mode of a bug is typically "the author fixes it in an hour," not "10,000 users file tickets."

## Signals That Indicate This Class

- 1-4 active committers in the last 12 months (`git shortlog -sne --since="12 months ago"`)
- Codebase is <20k LOC
- No published package on a public registry, or published but low-visibility
- README audience addresses the author ("TODO list") or a small group, not strangers
- Few or no external issues/PRs from outside the core committers
- User's invocation lens is `revisiting own repo`, `onboarding teammate`, `inheriting internal project`

## Counter-Signals (If Observed, Consider Another Class)

- Public package with many downstream consumers → probably `oss-library`
- Multi-service deployment with runtime operational concerns → probably `production-service`
- Frequent "experimental," "WIP," or "spike" commit messages → probably `prototype`

## Class-Relevant Strategic Concerns

- **Bus factor is the primary risk.** The code is only as maintainable as one person's ability to re-engage with it. Documentation and test coverage do double duty as externalized memory.
- **Tooling overhead should pay its own way.** Heavy CI, extensive mock infrastructure, or complex release automation are often over-investments for this class.
- **Pragmatic over idiomatic.** "Works for its users" beats "conforms to an industry standard" when there's tension.

## Dimension Rubrics

### Test Health

**Foundational** — Core invocation paths have either automated tests or a documented manual test procedure. A user can verify the tool still works after a change without reading the entire codebase.
*Signals:* tests exist at all (`tests/`, `*_test.go`, `test_*.py`, etc.); at least one test exercises the main entry point.

**Adequate** — Main invocation paths have automated tests; error paths and edge cases have targeted coverage where bugs have historically occurred. Tests run locally without special setup.
*Signals:* test-to-code LOC ratio ≥ ~0.15; tests cover entry points and primary command flows; `pytest` / `go test ./...` / equivalent runs cleanly.

**Strong** — Tests cover the specified behavior comprehensively, including error paths; new contributions customarily add tests; regressions are caught before merge.
*Signals:* coverage reports present and regularly referenced in commits or PRs; tests exercise both happy path and documented failure modes.

### Dependency Health

**Foundational** — Dependencies are declared (not implicit). The project builds/runs today from a clean checkout. Known-unmaintained or known-compromised packages are not present.
*Signals:* a lockfile or pinned manifest exists; `pip install`, `npm install`, `go mod download`, or equivalent succeeds on a fresh clone.

**Adequate** — Dependencies are lightly maintained. Most direct deps are within one major version of current; no known-abandoned packages in the tree.
*Signals:* `npm outdated` / `pip list --outdated` / equivalent shows <30% of direct deps more than one major behind; no deps flagged by audit tools (`npm audit`, `pip-audit`).

**Strong** — Dependencies are actively maintained. A disciplined upgrade cadence is visible in commits.
*Signals:* commit log shows periodic dep bumps; lockfile is refreshed; direct deps on current or near-current versions.

### CI / Automation Health

For this class, CI is optional at the Foundational level. The question is whether *some* path to reliable local verification exists, not whether GitHub Actions is configured.

**Foundational** — The author can run the test suite locally with a documented command. Manual verification happens before release, even if release is "push to main."
*Signals:* `make test`, `npm test`, or equivalent is documented in README or Makefile and actually works.

**Adequate** — CI runs on push or PR and gates at least the test suite. Broken builds are noticed and fixed within days, not months.
*Signals:* `.github/workflows/`, `.gitea/workflows/`, `.circleci/`, or equivalent present and recent runs are green.

**Strong** — CI gates merges, runs across the supported environments (e.g., OS/Python-version matrix), and includes additional checks (lint, type-check, security audit) beyond the bare test suite.
*Signals:* CI matrix exists; multiple job types beyond `test`; PR checks are visible and enforced.

### Documentation

**Foundational** — A README explains what the project is and how to use it — enough that a returning author six months later can re-enter the project without re-reading the source.
*Signals:* `README.md` (or equivalent) exists; covers installation and at least one usage example; is not stale relative to the code's current behavior.

**Adequate** — Installation, usage, and the primary configuration surface are documented. Common pitfalls are noted. Non-obvious design decisions are explained where the reader would predictably have questions.
*Signals:* README covers install, basic use, and configuration; inline comments mark non-obvious decisions; help text (`--help`) is informative.

**Strong** — Documentation anticipates the user's next question and answers it. Edge cases, troubleshooting, and rationale are accessible. A new contributor could make a meaningful change without asking the author.
*Signals:* README includes troubleshooting or FAQ; CHANGELOG or release notes present; contribution guidelines if accepting patches.

### Architecture Hygiene

**Foundational** — The code's structure is legible. A reader can identify the entry point, the main command surface, and where core logic lives within ten minutes.
*Signals:* entry points are discoverable (standard locations: `main.go`, `cli.py`, `bin/`); module boundaries exist at all; no single file >2000 LOC for core logic.

**Adequate** — Responsibilities are separated into modules with clear identities. Cross-module coupling is proportionate to the project's size. A reader can predict where new functionality would live.
*Signals:* module names describe their responsibility; most modules are <500 LOC; imports form a comprehensible graph without deep cycles.

**Strong** — The architecture is deliberately designed for this project's scale and purpose. Extension points are clear. Abstractions pay for themselves; accidental complexity is low.
*Signals:* the code's organization makes the project easy to extend in its intended directions; test organization mirrors code organization; naming is consistent across the codebase.
