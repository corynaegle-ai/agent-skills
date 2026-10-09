## What it does

Turn authorized conversation, spec, or ticket requirements into verified work. Record the starting revision and dirty state, test appropriately, and review all task-owned changes before the final commit.

## When to reach for it

Select explicitly for settled work that should be implemented. Existing project instructions and authorization govern commits and publication.

## Common questions

**Does the review see uncommitted work?**

Yes. It uses the task-start commit and worktree capture, including new files.

**Does this authorize a push or deployment?**

Only actions already authorized by the user or project workflow are performed. Each result is reported separately.

## It's working if

- Unrelated index/worktree changes are preserved.
- Actionable review findings are fixed and checked.
- The handoff identifies the resulting revision and actual checks.

## Where it fits

Read the [skill instructions](../../skills/engineering/implement/SKILL.md) for its workflow. [ask-matt](ask-matt.md) maps the wider library.
