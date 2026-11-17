#!/usr/bin/env python3
"""Mechanical checks for the plugin's skills, agents, and docs.

Run from the repo root (`make lint`). Exits non-zero on any failure.

Checks:
  frontmatter   skills/*/SKILL.md and agents/*.md open and close their YAML
                frontmatter and carry name, description, and a lowercase model;
                a skill's name matches its directory
  description   frontmatter descriptions stay within DESCRIPTION_MAX chars
  length        prompt and reference files stay within LINE_MAX lines
  tables        markdown table rows are padded to the same width
  agent-refs    every agent cited by id or display name exists
  skill-refs    every plugin skill cited as `/name` exists (removed skills may
                be named only on history lines: "v12", "formerly", "(now `/...`)")
  orphans       every agent is cited somewhere outside its own file
  modes         every mode a caller invokes is one the agent declares in
                `modes:`, and every declared mode appears in the agent body
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DESCRIPTION_MAX = 300
LINE_MAX = 500
MODELS = {"opus", "sonnet", "haiku", "fable"}
# Skill-name families this plugin owns; other slash commands (/compact,
# /code-review, /context, ...) belong to Claude Code and are not checked.
FAMILY = re.compile(
    r"`/((?:review|think|bug|tidy|test)-[a-z-]+|implement|scope|refactor|release|pre-compact)\b"
)
AGENT_ID = re.compile(r"`((?:swe|qa|sec|thk|ux|doc)-[a-z0-9-]+)`")
# Display names are cited quoted or backticked (`subagent_type: "THK - Advocate"`);
# bare matches would catch diagram headings such as "QA - VERIFY FIX".
AGENT_NAME = re.compile(r"""[`"]((?:SWE|QA|SEC|THK|UX|DOC) - [A-Z][A-Za-z0-9]*(?: [A-Z][A-Za-z0-9]*)*)[`"]""")
HISTORICAL = re.compile(r"v12|formerly|\(now `/", re.IGNORECASE)

errors = []
agent_modes = {}  # agent id -> normalized mode names it declares in frontmatter


def norm(text):
    """Compare mode names case- and hyphen-insensitively."""
    return re.sub(r"\s+", " ", text.lower().replace("-", " ").replace("*", ""))


def fail(path, line, check, msg):
    rel = path.relative_to(ROOT)
    errors.append(f"{rel}:{line}: [{check}] {msg}")


def frontmatter(path):
    lines = path.read_text().split("\n")
    if not lines or lines[0] != "---":
        fail(path, 1, "frontmatter", "file must open with ---")
        return {}
    try:
        end = lines.index("---", 1)
    except ValueError:
        fail(path, 1, "frontmatter", "frontmatter never closes with ---")
        return {}
    fields = {}
    for n, l in enumerate(lines[1:end], start=2):
        m = re.match(r"^([a-z_]+):\s*(.*)$", l)
        if m:
            fields[m.group(1)] = (m.group(2).strip().strip('"').strip("'"), n)
    return fields


skills = sorted(ROOT.glob("skills/*/SKILL.md"))
agents = sorted(ROOT.glob("agents/*.md"))
skill_names = {p.parent.name for p in skills}
agent_ids = {p.stem for p in agents}
agent_display = {}

for path in skills + agents:
    fm = frontmatter(path)
    for key in ("name", "description", "model"):
        if key not in fm:
            fail(path, 1, "frontmatter", f"missing `{key}`")
    if "model" in fm and fm["model"][0] not in MODELS:
        fail(path, fm["model"][1], "frontmatter", f"model must be one of {sorted(MODELS)} (lowercase)")
    if "description" in fm and len(fm["description"][0]) > DESCRIPTION_MAX:
        fail(path, fm["description"][1], "description",
             f"{len(fm['description'][0])} chars; max {DESCRIPTION_MAX}")
    if path in skills and "name" in fm and fm["name"][0] != path.parent.name:
        fail(path, fm["name"][1], "frontmatter", f"name `{fm['name'][0]}` != directory `{path.parent.name}`")
    if path in agents and "name" in fm:
        agent_display[fm["name"][0]] = path.stem
    if path in agents and "modes" in fm:
        raw, n = fm["modes"]
        if not (raw.startswith("[") and raw.endswith("]")):
            fail(path, n, "modes", "modes must be a flow list: modes: [a, b]")
        else:
            declared = [m.strip() for m in raw[1:-1].split(",") if m.strip()]
            agent_modes[path.stem] = {norm(m) for m in declared}
            body = norm(path.read_text().split("---", 2)[2])
            for m in declared:
                if norm(m) not in body:
                    fail(path, n, "modes", f"declared mode `{m}` never appears in the agent body")

# Files whose length is held to the house limit: prompts and reference docs.
bounded = skills + agents + sorted(ROOT.glob("references/*.md")) + sorted(ROOT.glob("skills/*/references/**/*.md"))
for path in bounded:
    n = path.read_text().count("\n")
    if n > LINE_MAX:
        fail(path, n, "length", f"{n} lines; max {LINE_MAX}")

docs = [p for p in ROOT.rglob("*.md") if not {".claude", ".git"} & set(p.relative_to(ROOT).parts)]

for path in docs:
    lines = path.read_text().split("\n")
    in_code = False
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith("```"):
            in_code = not in_code
        is_table = (
            not in_code
            and lines[i].lstrip().startswith("|")
            and i + 1 < len(lines)
            and "-" in lines[i + 1]
            and set(lines[i + 1].strip()) <= set("|-: ")
        )
        if is_table:
            j = i
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                j += 1
            widths = {len(lines[k].rstrip()) for k in range(i, j)}
            if len(widths) > 1:
                fail(path, i + 1, "tables", f"rows have different widths {sorted(widths)}; pad the columns")
            i = j
            continue
        i += 1

cited = set()
for path in docs:
    history = path.name == "CHANGELOG.md"
    for n, line in enumerate(path.read_text().split("\n"), start=1):
        for m in AGENT_ID.finditer(line):
            ident = m.group(1)
            if ident in agent_ids:
                if path.stem != ident:
                    cited.add(ident)
            elif not history and not ident.endswith("-") and not HISTORICAL.search(line):
                fail(path, n, "agent-refs", f"`{ident}` is not an agent")
        for m in AGENT_NAME.finditer(line):
            name = m.group(1)
            if name in agent_display:
                if path.stem != agent_display[name]:
                    cited.add(agent_display[name])
            elif not history and not HISTORICAL.search(line):
                fail(path, n, "agent-refs", f'"{name}" is not an agent display name')
        if history:
            continue
        for m in FAMILY.finditer(line):
            name = m.group(1)
            if name not in skill_names and not HISTORICAL.search(line):
                fail(path, n, "skill-refs", f"`/{name}` is not a skill (name the version if this is history)")

# Mode contracts: a caller that names an agent's mode must name one the agent
# declares. Two caller forms are checked, in skill prompts and runtime refs:
#   `Mode: X` in a dispatch prompt -> the nearest agent cited in the 30 lines above
#   "<agent> ... in X mode" prose  -> an agent cited on the same line
MODE_LINE = re.compile(r"\bMode:\s*\**([a-z][a-z -]*?)\**\s*(?:$|[.;,)—`]| —)")
MODE_PROSE = re.compile(r"\bin (?:its )?([a-z]+(?:-[a-z]+)*(?: [a-z]+)?) mode\b")
MODE_WINDOW = 30


def agents_on(line):
    found = [m.group(1) for m in AGENT_ID.finditer(line) if m.group(1) in agent_ids]
    found += [agent_display[m.group(1)] for m in AGENT_NAME.finditer(line) if m.group(1) in agent_display]
    return found


mode_refs = 0


def check_mode(path, n, agent, mode):
    global mode_refs
    mode_refs += 1
    if agent not in agent_modes:
        fail(path, n, "modes", f"invokes `{agent}` in mode `{mode}`, but the agent declares no modes")
    elif norm(mode) not in agent_modes[agent]:
        fail(path, n, "modes", f"`{agent}` has no mode `{mode}` (declares: {', '.join(sorted(agent_modes[agent]))})")


callers = sorted(ROOT.glob("skills/*/SKILL.md")) + sorted(ROOT.glob("skills/*/references/**/*.md"))
for path in callers:
    lines = path.read_text().split("\n")
    for n, line in enumerate(lines, start=1):
        m = MODE_LINE.search(line)
        if m:
            near = []
            for k in range(n, max(0, n - 1 - MODE_WINDOW), -1):
                near = agents_on(lines[k - 1]) if k != n else agents_on(line[: m.start()])
                if near:
                    break
            if near:
                check_mode(path, n, near[-1], m.group(1).strip())
        for m in MODE_PROSE.finditer(line):
            on_line = agents_on(line[: m.start()])
            if on_line:
                check_mode(path, n, on_line[-1], m.group(1))

for ident in sorted(agent_ids - cited):
    fail(ROOT / "agents" / f"{ident}.md", 1, "orphans", "no skill, agent, or doc cites this agent")

if errors:
    print("\n".join(errors))
    print(f"\nlint: {len(errors)} problem(s)")
    sys.exit(1)
print(f"lint: ok ({len(skills)} skills, {len(agents)} agents, {len(docs)} docs, {mode_refs} mode references)")
