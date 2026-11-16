# /review-a11y - Accessibility Audit

The step-by-step procedure lives in [`SKILL.md`](../SKILL.md); this guide covers when to use the skill and what to expect.

## Overview

`/review-a11y` audits web content (HTML, JSX/TSX, Vue, Svelte, stylesheets, HTML templates) against WCAG 2.2 Level AA and produces a report prioritized by real-world user impact.

Why it's shaped this way:

- **Impact over compliance.** A missing form label that blocks screen-reader users matters more than a redundant ARIA role that harms nobody. Issues are ranked by how badly they affect people using assistive technology, not by checklist position.
- **Automated plus manual.** The auditor runs automated tooling (axe-core, pa11y) when it's available, then inspects by hand for what tools miss: keyboard navigation, semantic structure, ARIA usage, dynamic content, forms and errors, contrast, pointer input, and media.
- **Diagnostic, not therapeutic.** It recommends fixes and never implements them.

```
Detect web content ──▶ Scope ──▶ Auditor(s), partitioned in parallel for large scopes ──▶ Consolidated report
```

## When to Use

**Use `/review-a11y` for:**
- Evaluating the accessibility posture of a web project
- Pre-release checks for WCAG conformance
- Auditing after significant UI changes
- Understanding what assistive-technology users experience

**Don't use `/review-a11y` for:**
- Non-web projects (CLI tools, APIs, libraries without UI): the skill finds no web content and stops
- Implementing fixes: ask directly after reviewing findings, or use `/implement`
- Strategic orientation on an unfamiliar repo: `/review-repo`
- Performance or security: `/review-perf`, `/review-security`

**Rule of thumb:** if you want to know "can people with disabilities use this?", use `/review-a11y`.

## What You'll Be Asked

Unless the invocation or a caller (such as `/review-repo`'s follow-up) supplies scope, the skill shows the web content it detected, with file counts, and asks what to audit: the entire project (default), a directory, or specific files.

## What You Get Back

A consolidated report, inline:

- The conformance target, the method used (automated, live browser, and manual, or manual inspection only), and the scope.
- Issues by severity: **CRITICAL** (blocks access entirely), **HIGH** (significantly degrades the experience), **LOW** (minor issue or enhancement). Each names the affected users, the WCAG criterion, and a specific fix.
- AAA opportunities, listed separately and never counted against AA conformance.
- Tooling recommendations and suggested next steps, noting which fixes are HTML, CSS, or JS changes.

Patterns across the codebase (for example, missing labels as a project-wide habit) are called out rather than listed as isolated incidents. "No significant barriers" is a valid result. The skill is read-only and lightweight, and it proposes no tickets; under `/review-repo`'s follow-up, its findings feed that skill's consolidated ticket set.
