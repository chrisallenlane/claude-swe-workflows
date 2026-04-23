# Reference Class: Prototype / Research Codebase

An exploratory codebase: a research project, a spike, an experiment, a proof-of-concept, or pre-production work that has not been committed to as a long-lived artifact. The project's purpose is learning, not serving. Trading production-grade discipline for iteration speed is a legitimate choice at this stage, not a failing.

## Signals That Indicate This Class

- Commit messages include "experiment," "spike," "WIP," "hack," "try," "exploring"
- README or equivalent acknowledges the prototype status ("WIP," "research code," "not for production," "exploring X")
- No published releases, no versioning discipline
- Often notebook-heavy (`.ipynb`, `notebooks/`) or script-driven
- Short history, or long history with frequent architectural resets
- User's invocation lens is `evaluating for production-hardening` or `revisiting own repo` after explicit acknowledgment that the repo was exploratory

## Counter-Signals (If Observed, Consider Another Class)

- Deployment infrastructure, on-call setup, production users → probably `production-service`
- Published package with external consumers → probably `oss-library`
- Active long-term use even if "internal" → probably `solo-utility`

## Class-Relevant Strategic Concerns

- **Discipline-for-its-own-sake is a miscalibration.** Demanding 80% coverage of a research prototype is demanding the wrong thing. The class rubric reflects this.
- **The strategic question is usually "is this ready for promotion?"** — to `solo-utility`, `production-service`, or `oss-library`. The review's output should help the user answer that.
- **What *is* here matters more than what isn't.** Findings should identify what the prototype has demonstrated, what it's decided (explicitly or implicitly), and what would need to change if promoted — not penalize it for absent production-grade ceremony.
- **Reproducibility is a reasonable baseline.** Even exploratory work should be runnable by someone other than the author after a reasonable time away. A prototype no one can re-run has lost most of its value.

## Dimension Rubrics

### Test Health

**Foundational** — Some form of verification exists, even if informal. The author can demonstrate the prototype's claims. This may be a notebook that runs end-to-end, a sample script, or a handful of assertions — not necessarily a formal test suite.
*Signals:* at least one runnable artifact that exercises the prototype's central claim; `examples/`, `demo.py`, a reproducible notebook, or a small `tests/` directory exists.

**Adequate** — Core logic (the parts that would survive promotion) has targeted tests or assertion-heavy scripts. The author has made some effort to externalize verification beyond "I ran it once and it looked right."
*Signals:* tests or verification scripts for the modules representing the prototype's non-throwaway work; some structure to how the prototype is verified (a `run.sh`, Makefile, or equivalent).

**Strong** — Tests exist at the level of rigor appropriate for promoting the prototype. The core logic is tested such that promotion to `production-service` or `oss-library` would not require rewriting the verification layer.
*Signals:* core-logic coverage is substantive (not exhaustive); tests cover the prototype's decisions, not just its happy path; verification is automatable.

### Dependency Health

**Foundational** — Dependencies are declared enough that the prototype is reproducible. A fresh clone can be brought to a running state using the documented procedure (even if that procedure is informal).
*Signals:* `requirements.txt`, `environment.yml`, `package.json`, `Pipfile`, or equivalent exists; the install procedure is documented, even if briefly.

**Adequate** — Dependencies are pinned or lockfiled so reproducibility is not subject to upstream drift. Known-unmaintained packages are avoided for core functionality.
*Signals:* lockfile present; no deps that are trivially replaceable but known-abandoned.

**Strong** — Dependencies reflect intent. The prototype's core deps are the ones it actually needs for its claims, not accreted junk. Supply-chain posture is acceptable if promoted.
*Signals:* small, intentional dep set; no egregious CVEs; transitive deps are not obviously problematic.

### CI / Automation Health

For this class, CI is genuinely optional. Absence is not a finding. The question is whether *some* mechanism exists for the author to check the prototype hasn't broken.

**Foundational** — The prototype can be run from a clean clone following documented steps. There is a procedure; it may be manual.
*Signals:* documented run procedure (README, Makefile, notebook with instructions); the procedure actually works.

**Adequate** — A lightweight automation exists for running whatever verification the prototype has. This may be a CI workflow running a notebook end-to-end, a `make check` target, or a scheduled re-run.
*Signals:* CI present but scoped appropriately (may just run a single smoke test); or a well-kept Makefile / script with `test` / `verify` / `run` targets.

**Strong** — Automation is configured such that the prototype's verification runs on a schedule or on change. Environment rot is noticed before it becomes blocking.
*Signals:* CI runs on PR or schedule; environment file is tracked and current; verification is runnable by someone other than the author.

### Documentation

**Foundational** — The prototype's *purpose* is documented. A reader can answer: what is this trying to demonstrate, what has it shown, what remains open? This is the minimum for a prototype to retain value beyond its author's attention.
*Signals:* README or equivalent states the research question or goal; there is some indication of status (works / partial / abandoned / promoted).

**Adequate** — Key decisions, what was tried and didn't work, and the current state of the exploration are documented. A returning author (or successor) can resume work without re-running every experiment.
*Signals:* notes on decisions, parameter choices, or rejected approaches; results captured alongside code (or explicitly referenced); RESULTS.md, NOTES.md, or notebook prose.

**Strong** — Documentation supports handoff. Another researcher could pick up the prototype and extend it, or a production team could understand what would need to change for promotion. Findings are explicit.
*Signals:* promotion guide or known-gaps list present; findings or conclusions documented clearly; next-step recommendations for the prototype's trajectory.

### Architecture Hygiene

**Foundational** — The prototype is navigable. A reader can find the entry point, identify the main claims, and locate where the interesting logic lives. Notebook-heavy prototypes: notebooks are organized, not a pile of `Untitled*.ipynb`.
*Signals:* entry points are discoverable; notebooks or scripts have descriptive names; a reader can construct a mental model in reasonable time.

**Adequate** — Structure distinguishes exploratory scaffolding from the work that would survive promotion. The author has started separating "load/preprocess/visualize" plumbing from the core logic.
*Signals:* modular separation between data/preprocessing/modeling/evaluation (where applicable); reusable utilities extracted from notebooks into modules; entry points are explicit.

**Strong** — The prototype's architecture is pre-production-ready. Promotion to the appropriate next class would require porting the build/CI/docs, not rewriting the core. Accidental complexity has been kept low.
*Signals:* module layout would plausibly survive promotion; core logic is decoupled from exploratory scaffolding; naming reflects intent.
