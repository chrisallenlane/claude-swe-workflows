# Severity Tiers for Individual Findings

Borrowed from the American Society of Home Inspectors (ASHI) defect-severity taxonomy, adapted for source-code artifacts. Every individual finding produced by `/review-health` carries exactly one severity tier.

Severity tiers are **independent of reference class**. A finding's severity is a claim about its intrinsic consequences, not about whether it's expected-for-this-kind-of-repo. (The latter is what the class rubric handles.) A `Major` finding in an OSS library may represent a different strategic response than a `Major` finding in a prototype — but it's a `Major` finding in both cases.

## The Four Tiers

### Safety Hazard

A condition that creates material risk of harm to the project, its users, or its maintainers if left as-is. Typically: exploitable in production, causes data loss or corruption, legally exposes the project, or will predictably cause outages. Safety findings warrant immediate attention regardless of the user's lens.

**Criteria:**
- Known-exploitable vulnerability in a directly reachable code path
- Unreviewed secrets committed to history (tokens, keys, credentials)
- Data-integrity hazard (missing migrations, incorrect constraints, unhandled concurrency)
- License violation that exposes the project legally
- CI/build is broken and has been broken long enough that recovery is non-trivial

**Examples:**
- `.env` file containing production API keys is committed at `.env:12`
- `requirements.txt:23` pins `requests==2.19.1` — a version with a documented unpatched CVE in the reachable code path
- `src/db/migrate.py` writes to production schema without a rollback path

### Major

A condition that materially impedes understanding, modification, or confidence in the codebase — but does not by itself create safety risk. Major findings are the primary content of most strategic-orientation reports: they're what the user needs to know to make decisions about engagement.

**Criteria:**
- Core functionality is untested or meaningfully under-tested
- Dependencies are severely stale or include known-deprecated packages
- Architectural pattern is incoherent at a scale that blocks modification
- Documentation of the project's purpose, contract, or behavior is absent or actively misleading
- CI is nominally present but doesn't meaningfully gate merges

**Examples:**
- `src/payments/` has no tests; observed by absence of `tests/payments/` and no matches for `payments` in `pytest` output
- `package-lock.json:*` shows 43% of dependencies are more than two major versions behind current
- README claims REST API; code implements GraphQL (`src/api/schema.graphql:1`)

### Minor

A condition that is suboptimal but does not block engagement. The user can proceed and address the finding at their convenience, or accept it as part of the project's current state. Minor findings populate the "watch" category, not the "act" category.

**Criteria:**
- Test coverage is thin in a non-critical area
- A handful of dependencies are outdated but not severely so
- Code style or naming is inconsistent in pockets
- Some modules have low-signal documentation where better would help but current isn't harmful

**Examples:**
- `src/util/string_helpers.py` has no unit tests (but is low-complexity, low-usage)
- `go.mod:14-19` shows six direct dependencies one minor version behind
- `src/auth/` uses `camelCase` while the rest of the codebase uses `snake_case`

### Cosmetic

A condition that is observable but functionally irrelevant. Cosmetic findings are reported for completeness but do not warrant user attention unless a higher-severity finding brings the area into focus. These are typically aggregated rather than enumerated.

**Criteria:**
- Trailing whitespace, minor formatter disagreements
- Comments that are outdated but don't mislead
- File-organization quirks without downstream consequence

**Examples:**
- 12 files contain trailing whitespace inconsistent with `.editorconfig`
- `src/legacy/old_api.py` has a copyright header dated 2018 — not stale in any load-bearing sense

## How Severity Relates to Class Rubric Placement

The class rubric answers: **is this dimension at Foundational / Adequate / Strong for this class of repo?** Severity answers: **how consequential is this specific finding, independent of class?**

The two are independent. A `Major` finding can coexist with a dimension rated `Adequate` (the dimension is class-appropriate overall, but this one finding within it is still material). Conversely, a `Foundational` rating on a dimension will typically contain one or more `Major` or `Safety` findings — that's why it scored Foundational.

When reporting, lead with Safety Hazards, then Major findings, then Minor. Cosmetic findings should be aggregated or omitted unless the user explicitly asks for them.

## Evidence Discipline

Every finding — at every severity tier — must carry a `file:line` citation or a tool-output reference. This is not a stylistic convention; it is a structural requirement. A finding without citable evidence is not a finding; it is an unsupported assertion and must be dropped or downgraded to a "could not verify" entry in the Coverage Manifest.
