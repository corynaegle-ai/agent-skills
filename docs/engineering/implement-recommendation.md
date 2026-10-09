## What it does

`implement-recommendation` turns one numbered architecture recommendation into verified changes in the current project. It resolves the candidate from the current conversation or a supplied report, verifies the proposal against current code, and follows the project's coding workflow, including `CODING_WORKFLOW.md` when present.

The saved instructions cover design refinement, implementation, appropriate testing, review, fixes, and authorized commits/pushes. The skill preserves unrelated work and existing behavior unless the selected recommendation explicitly requires a behavior change.

## When to reach for it

Use it after reviewing an architecture report and deciding which candidate to implement. In Claude Code, run `/implement-recommendation 1`. In Codex CLI or IDE, use `$implement-recommendation 1`. Replace `1` with the candidate number.

In a new conversation, also supply the report path, for example `/implement-recommendation 2 /tmp/architecture-review-example.html`. The number selects one candidate; it does not authorize implementing the whole report.

For a survey first, use [improve-codebase-architecture](./improve-codebase-architecture.md). For general conversation, spec, or ticket work, use [implement](./implement.md).

## Common questions

**Does it pick a recommendation if I omit the number?**

No. It asks for the number. A missing report, ambiguous source, or out-of-range selection must also be resolved before edits. It does not search temporary files for an assumed latest report.

**Will it work outside Synari?**

Yes. It uses the current project's instructions and coding workflow rather than a hard-coded project path.

**Does the report-only restriction still apply?**

Invoking this skill authorizes implementation of the selected recommendation. The architecture survey remains report-only. Publication and deployment follow existing task authorization and project instructions.

**What if the report is outdated?**

The skill checks the proposal against current code. If the friction has disappeared or a material architectural decision remains unresolved, it explains the evidence before changing code.

## It's working if

- It identifies the selected number, candidate title, and source before editing.
- It follows the current project's coding workflow and implements only the selected candidate.
- It preserves unrelated changes and checks the completed work, including new files.
- Its handoff states actual validation results, limitations, and commit/push status.
