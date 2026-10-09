---
name: implement
description: "Implement authorized work from a conversation, spec, or ticket, then verify and review the completed changes."
disable-model-invocation: true
---

Implement the authorized work described by the conversation, spec, or ticket. Fetch any supplied tracker reference and state its title; ask if the reference is ambiguous. Reuse settled decisions.

Before editing, record the task-start commit, dirty paths, and staged changes. Preserve unrelated work and use an isolated branch/worktree when needed. Identify acceptance criteria and existing test boundaries.

Load `tdd` for behavioral changes that warrant new tests. Use the available skill tool or read the installed skill's `SKILL.md` and conditional references. Run focused checks while changing code, then the repository's required checks and relevant integration suite on the completed result. State unavailable checks and their practical limits.

Load `code-review` with the task-start commit, worktree scope, acceptance criteria, and paths owned by this task. Review staged, unstaged, and new files before the final commit. Fix actionable findings within scope, verify each correction, and rerun affected checks. Use an independent reviewer when available and permitted; otherwise disclose shared context.

Commit task-owned changes when authorized by the user or project workflow. Stage named paths or hunks and preserve the unrelated index/worktree. Pushes, issue closure, PR publication, deployment, signing, and physical acceptance are separate actions and claims. Perform those already authorized and required by the task, and report their actual results.
