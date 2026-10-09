---
name: implement-recommendation
description: Implement a numbered architecture recommendation from the current conversation or a supplied report, following the project's coding workflow.
argument-hint: "<number> [report-path]"
disable-model-invocation: true
---

# Implement Recommendation

Implement only the selected architecture recommendation in the current project. The invocation supplies a positive recommendation number and optionally a report path. In hosts that expand arguments, these arrive as `$ARGUMENTS`; otherwise read them from the user's invocation message.

## Resolve the recommendation

Use the supplied report when present; otherwise use the architecture report already identified in the current conversation. Read the selected candidate's problem, proposed solution, file references, tradeoffs, diagrams, and any settled design decisions. If an older report has unnumbered cards, use their displayed order starting at 1.

State the selected number, candidate title, and source before editing. If the number is missing, invalid, or out of range, or the report is missing or ambiguous, ask for the missing selection or source. A bare invocation must not select a candidate on the user's behalf. Do not guess a report by scanning temporary files or selecting the newest file.

## Implement the selected work

Read the project's `AGENTS.md`/`CLAUDE.md`, glossary, and relevant ADRs. If `CODING_WORKFLOW.md` exists or the project instructions point to another coding workflow, read and follow it for this implementation. Work in the current project; the report is a proposal to verify against current code, not authority to bypass project instructions.

Record the starting commit, dirty paths, and staged changes. Preserve unrelated work and use an isolated branch/worktree when needed. Confirm that the candidate belongs to this project and still addresses real friction. Reuse settled decisions; ask only about unresolved choices that materially affect the implementation. If the proposal is obsolete or contradicts an unresolved architectural decision, explain the evidence before changing code.

Refine the design and state acceptance criteria, then implement the selected recommendation. Preserve existing behavior unless the selected recommendation explicitly requires a behavior change. Use `codebase-design` when refining module interfaces. Leave other recommendations for separate tasks.

## Verify and finish

Use `tdd` for behavioral changes that warrant new tests. Run focused checks, the project's required checks, and relevant integration tests. Use `code-review` with the starting commit, worktree scope, acceptance criteria, and task-owned paths so it includes staged, unstaged, and new files. Fix actionable findings and rerun affected checks. Use an independent reviewer when available and permitted; otherwise disclose shared review context.

Use the available skill tool for those model-invoked skills, or read their installed `SKILL.md` and relevant references directly.

Commit and push task-owned changes when authorized by the user or required by the project's coding workflow, preserving unrelated index/worktree changes. Perform other external actions only within existing task authorization. Report the selected recommendation, what changed, actual validation results and limitations, and commit/push status. Report deployment, signing, and device acceptance separately when applicable.
