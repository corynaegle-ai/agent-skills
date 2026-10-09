## What it does

`improve-codebase-architecture` reviews the current project for **deepening opportunities**: places where a lot of behavior could sit behind a smaller interface. The default invocation needs no additional prompt. Unless you name a scope, it uses recent Git history to select one frequently changed subsystem.

By default, it presents up to three worthwhile improvements in an HTML report. Pass `full` to review the entire project, including stable and older code. Full mode maps the major applications, shared packages, other owned source areas, and their dependencies, examines each area, and reports all worthwhile findings ranked by impact and effort. Its coverage summary names examined areas and anything unchecked, blocked, or excluded.

Both modes include actual files and call sites, the current friction, a proposed change, tradeoffs, testing benefits, before/after diagrams, and recommendation strength. Each candidate must pass the deletion test: complexity should concentrate behind the proposed interface rather than spread across callers. If none is worthwhile, the report says so.

The report is written to `<tmpdir>/architecture-review-<timestamp>.html` and opened in your browser. The agent reports the absolute path and stops. Repository files, tickets, and Git state remain unchanged.

## When to reach for it

Use it for a first architecture survey, before a feature that will touch a difficult subsystem, or when tests are hard to write through existing interfaces. Invoke the installed skill in the target project's session. In Claude Code, use `/improve-codebase-architecture`; in Codex CLI or IDE, use `$improve-codebase-architecture` or the skill picker.

You can supply a subsystem, pain point, or upcoming feature to override the default scope. For a known broken behavior, start with [diagnosing-bugs](./diagnosing-bugs.md). For an already chosen module's design, use [codebase-design](./codebase-design.md).

For a whole-project review, use `/improve-codebase-architecture full` in Claude Code or `$improve-codebase-architecture full` in Codex CLI or IDE. The leading keyword selects full mode without a longer prompt.

## Common questions

**Do I need to paste a review prompt every time?**

No. The report-only defaults are embedded in the skill. They apply to the current project, including Synari, without hard-coding a project name or path.

**Does it require a glossary or ADRs?**

No. It reads `GLOSSARY.md` and relevant ADRs when present and uses the project's domain vocabulary. The report-only run leaves those documents unchanged.

**Does full mode still focus on recent changes or stop at three recommendations?**

No. It examines every major owned source area and includes all worthwhile findings. Git history supplies context rather than restricting scope. If the review cannot finish, the coverage summary explicitly identifies unchecked or blocked areas; full mode is not a claim that unfinished work has been reviewed.

**Does it start an interview or make changes?**

The default run stops after the report. Request a design interview about a candidate to explore constraints, dependencies, interfaces, and testing through [grilling](../productivity/grilling.md). Proposed glossary and ADR changes stay in the conversation unless you authorize documentation edits. Implementation is a separate task.

**How do I implement one of the recommendations?**

Candidates are numbered from 1 in display order. Use [implement-recommendation](./implement-recommendation.md) with the selected number in the same conversation, or supply both the number and report path in a new one.

**Why are the report's styling or diagrams missing?**

The default report loads Tailwind and Mermaid from CDNs, so those assets need network access. For an offline or restricted browser, request inline CSS and SVG diagrams instead.

**How do I judge whether the skill is useful?**

Check whether its findings identify real maintenance friction, cite concrete callers, and explain why the proposed interface reduces complexity. A useful report includes costs and testing implications, and can conclude that no refactor is worthwhile. Structural repository checks do not prove the quality of its architectural judgment.

## It's working if

- A bare invocation reviews the current project and selects one subsystem from recent changes unless you supplied a scope.
- A default review presents at most three worthwhile candidates, or explains why none qualifies.
- A `full` review maps the project and dependencies, includes stable and older areas, and presents every worthwhile finding ranked by impact and effort.
- Full-mode coverage names examined areas and any unchecked, blocked, or excluded work with paths and reasons.
- Each candidate cites real files and call sites, includes before/after diagrams, and explains tradeoffs and testing benefits.
- The report opens from the OS temporary directory, and the agent supplies its absolute path.
- Repository files, tickets, and Git state remain unchanged during the report-only run.
- It stops after the report and starts a design interview only when requested.
