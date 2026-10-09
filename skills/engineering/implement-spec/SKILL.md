---
name: implement-spec
description: "Implement a spec as bounded parallel tickets on an integration branch, then review and verify the combined result."
disable-model-invocation: true
---

Build the authorized spec and its ticket graph on one integration branch. Read existing tracker configuration when needed; supplied local tickets are sufficient. Use the project's glossary and relevant ADRs.

## Prepare

Record the starting revision, dirty paths, acceptance criteria, and required lint, type, build, test, and integration commands. Preserve unrelated work. Create an integration branch and record its base commit.

Track a ticket as ready when every blocker has landed on the integration branch and passed its merge checks. Issues may remain open until the PR merges: compute readiness from landed commits, not issue-closure counts. Flag missing or cyclic dependencies before starting affected tickets.

## Build the ready frontier

Use implementer subagents when delegation is available and permitted; otherwise work sequentially. Limit active implementers to the lower of three, available capacity, and any user/project limit. Include merger/reviewer agents in the total capacity. Serialize overlapping file ownership and shared schema/contract changes even when declared blockers are empty.

Give each implementer its ticket, acceptance criteria, owned paths, test boundaries, integration revision, and necessary references. Each works in its own worktree and branch based on the integration branch. Verify its starting revision; create a fresh worktree instead of resetting dirty work. Implementers are leaf workers and do not dispatch agents.

Each worker loads the installed `tdd` skill using the available skill tool or by reading its `SKILL.md`. Existing authorization and test boundaries carry into workers. Run relevant checks, commit only owned changes, and report the commit, checks, and unresolved issues.

Serialize integration merges. Refresh from the integration tip, resolve conflicts with knowledge of both tickets, and run checks for affected interfaces after every merge before releasing dependent tickets. Failed checks pause dependent work while independent work can continue. Preserve failed worktrees and findings for recovery.

## Review and verify the combined result

After all tickets land, load `code-review` against the recorded integration base. Use branch scope for clean committed work or worktree scope for uncommitted fixes. Both axes review the same frozen snapshot. Reviewers are leaf workers.

Fix actionable findings within the spec, verify targeted failures, and commit fixes. Rerun affected checks after corrections. Repeat focused review for new or unresolved risks; avoid restarting a broad review without new evidence.

On the final integrated revision, run the repository's required lint, typecheck, build, test suite, and relevant end-to-end/integration checks. Exercise acceptance scenarios across ticket boundaries. Record exact commands, outcomes, revision, and skipped checks. Worker checks alone cannot establish integration success. A required check that fails or cannot run leaves the PR draft and affected tickets unresolved.

## Close out

Open or update a PR only within existing authorization. Tracker settings alone do not grant permission to publish. An authorized PR can start as a draft after the first commit; mark it ready after combined checks and actionable findings pass. Load `pr` to shape its description through the available skill tool or installed `SKILL.md`.

Reconcile acceptance criteria with the integrated result. Close tickets through the authorized tracker workflow; where closure occurs on merge, link them to the PR and leave them open until then. Distinguish source, local checks, CI, signing/release, deployment, and device acceptance.

Remove only task-created worktrees that are clean and whose commits have landed. Preserve dirty, failed, or unmerged worktrees and report their paths. Report the integration branch/revision, completed/remaining ticket counts, and any remaining required action.
