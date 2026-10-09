---
name: improve-codebase-architecture
description: Review architecture in a visual HTML report; use full for the whole codebase or omit it for a focused review.
argument-hint: "[full] [scope]"
disable-model-invocation: true
---

If the host has no Skill tool, read the named installed skill’s `SKILL.md` and relevant references directly.


# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

## Invocation modes

Resolve the mode before choosing where to look. Read the invocation arguments from `$ARGUMENTS` when the host expands them, or from the user's invocation message otherwise. A leading standalone `full` argument selects the full invocation below; it is a mode keyword, not a subsystem name. Without `full`, use the default invocation. A path or phrase that merely contains the word "full" does not select full mode.

### Default invocation

Review the current project. Use recent Git history to select one frequently changed subsystem unless the user specifies a scope.

Present up to three worthwhile improvements with concrete file and call-site references, tradeoffs, testing benefits, and before/after diagrams. Generate the HTML report in the OS temporary directory and open it.

Leave repository files, tickets, and Git state unchanged. Stop after the report; begin the design interview only when requested. If no worthwhile opportunities exist, say so rather than inventing candidates.

### Full invocation

For `improve-codebase-architecture full`, apply this embedded prompt:

```text
Review the entire project codebase.

Override the default focus on one recently changed subsystem.
Map the major applications, shared packages, and their dependencies,
then examine each area for architectural friction.

Include stable and older code. Remove the three-recommendation limit
and report all worthwhile findings, ranked by impact and effort.

Include a coverage summary showing which areas were examined and
which remain unchecked. Keep the run report-only.
```

Both modes preserve repository files, tickets, and Git state, write the report outside the repository, open it, and stop. The full invocation overrides the default scope and candidate limit. It does not start the design interview or authorize implementation. If no worthwhile opportunities exist, report that finding.

## Shared design context

This command is _informed_ by the project's domain model and built on a shared design vocabulary:

- Call the Skill tool with "codebase-design" for the architecture vocabulary (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**) and its principles (the deletion test, "the interface is the test surface", "one adapter = hypothetical seam, two = real"). Use these terms exactly in every suggestion, and don't drift into "component," "service," "API," or "boundary."
- The domain language in `GLOSSARY.md` gives names to good seams; ADRs in `docs/adr/` record decisions this command should not re-litigate.

## Process

### 1. Explore

**Scope before you scan: YAGNI.** Decide where to look using the selected invocation mode:

- **Full:** inventory the project's major applications, shared packages, other owned source areas, and their dependencies. Examine each area, including stable and older code. Use recent history as context without restricting coverage. Keep a ledger of area/path, dependencies, review status, and remaining work across exploration passes. Name exclusions such as generated or vendored code. If limits prevent completion, identify unchecked or blocked areas and their reasons rather than claiming a complete review.
- **Default with a named direction** (a module, subsystem, or pain point): use that scope and skip history-based inference.
- **Default without a named direction:** walk back a good stretch of the commit history (`git log --oneline`) to find the files and areas that keep coming up. Select one frequently changed subsystem for this review. If no clear hot spot emerges, choose one coherent subsystem and explain the choice in the report.

Read the project's domain glossary (`GLOSSARY.md`) and any ADRs in the area you're touching first.

Then spawn a sub-agent to walk the codebase. Don't follow rigid heuristics; explore organically and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow**, with an interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it? A "yes, concentrates" is the signal you want.

### 2. Present candidates as an HTML report

Write a self-contained HTML file to the OS temp directory so nothing lands in the repo. Resolve the temp dir from `$TMPDIR`, falling back to `/tmp` (or `%TEMP%` on Windows), and write to `<tmpdir>/architecture-review-<timestamp>.html` so each run gets a fresh file. Open it for the user (`xdg-open <path>` on Linux, `open <path>` on macOS, `start <path>` on Windows) and tell them the absolute path.

The report uses **Tailwind via CDN** for layout and styling, and **Mermaid via CDN** for diagrams where a graph/flow/sequence reliably communicates the structure. Mix Mermaid with hand-crafted CSS/SVG visuals: use Mermaid when relationships are graph-shaped (call graphs, dependencies, sequences), and hand-built divs/SVG when you want something more editorial (mass diagrams, cross-sections, collapse animations). Each candidate gets a **before/after visualisation**. Be visual.

For each candidate, render a card with:

- **Recommendation number**: sequential from 1 in display order; use the same number in the report and conversation so the user can select it with `implement-recommendation`
- **Files**: which files/modules are involved
- **Problem**: why the current architecture is causing friction
- **Solution**: plain English description of what would change
- **Benefits**: explained in terms of locality and leverage, and how tests would improve
- **Tradeoffs**: costs, risks, and when the change would not pay off
- **Before / After diagram**: side-by-side, custom-drawn, illustrating the shallowness and the deepening
- **Recommendation strength**: one of `Strong`, `Worth exploring`, `Speculative`, rendered as a badge

In full mode, include the project/dependency map and coverage summary from the exploration ledger. Show examined, unchecked, blocked, and excluded areas with paths and reasons where applicable. Include every worthwhile finding without the default three-candidate cap. Give each finding an impact and effort estimate with a short rationale, then rank by impact first and effort second. Assign recommendation numbers after ranking so report order and follow-up selections agree.

End the report with a **Top recommendation** section: which candidate you'd tackle first and why. If no candidate is worthwhile, explain that finding instead.

**Use GLOSSARY.md vocabulary for the domain, and the `/codebase-design` vocabulary for the architecture.** If `GLOSSARY.md` defines "Order," talk about "the Order intake module," not "the FooBarHandler," and not "the Order service."

**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting the ADR. Mark it clearly in the card (e.g. a warning callout: _"contradicts ADR-0007, but worth reopening because…"_). Don't list every theoretical refactor an ADR forbids.

See [HTML-REPORT.md](HTML-REPORT.md) for the full HTML scaffold, diagram patterns, and styling guidance.

Do NOT propose interfaces yet. After opening the report, tell the user its absolute path and stop. The user can request a design interview about a candidate in a follow-up.

### 3. Grilling loop

Only when the user requests a design interview about a candidate, call the Skill tool with "grilling" to walk the decision tree with them: constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive. Picking a candidate for discussion does not authorize implementation or repository edits.

Keep proposed glossary and ADR changes in the conversation unless the user authorizes documentation edits. When those edits are authorized, call the Skill tool with "domain-modeling" to keep the domain model current as decisions crystallize:

- **Naming a deepened module after a concept not in `GLOSSARY.md`?** Add the term to `GLOSSARY.md`. Create the file lazily if it doesn't exist.
- **Sharpening a fuzzy term during the conversation?** Update `GLOSSARY.md` right there.
- **User rejects the candidate with a load-bearing reason?** Offer an ADR, framed as: _"Want me to record this as an ADR so future architecture reviews don't re-suggest it?"_ Only offer when the reason would actually be needed by a future explorer to avoid re-suggesting the same thing; skip ephemeral reasons ("not worth it right now") and self-evident ones.
- **Want to explore alternative interfaces for the deepened module?** Call the Skill tool with "codebase-design" and use its design-it-twice parallel sub-agent pattern.
