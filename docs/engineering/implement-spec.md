## What it does

Build a ticket graph on one integration branch with bounded workers and serialized merges. Final checks exercise the combined result, not just individual ticket branches.

## When to reach for it

Select explicitly for a spec with dependent tickets. Delegation must be permitted; otherwise the same graph can be worked sequentially.

## Common questions

**How much parallel work runs?**

At most three implementers, constrained further by host capacity and user/project limits. Shared file or contract ownership is serialized.

**When is a dependent ticket ready?**

After its blockers have landed and passed merge checks. An issue may remain open until the eventual PR merge.

**What happens when a required check cannot run?**

Report the limitation, preserve recovery worktrees, and leave the PR draft and affected tickets unresolved.

## It's working if

- The final integrated revision has recorded checks and cross-ticket acceptance evidence.
- PR readiness follows successful combined verification.
- Dirty, failed, and unmerged worktrees survive cleanup.

## Where it fits

Read the [skill instructions](../../skills/engineering/implement-spec/SKILL.md) for its workflow. [ask-matt](ask-matt.md) maps the wider library.
