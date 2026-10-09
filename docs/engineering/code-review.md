## What it does

Review committed or uncommitted work against repository standards and requested behavior. Both axes use the same frozen snapshot. Worktree review includes staged, unstaged, and non-ignored untracked files, so it works before committing.

## When to reach for it

Use for PRs, branches, or work in progress. It can be explicitly selected or loaded when a review task fits. The current conversation or local spec is enough; tracker setup is optional.

## Common questions

**Does it see new files before a commit?**

Yes. The private snapshot records untracked contents separately and captures index/worktree patches without changing either.

**Can reviewers recursively spawn agents?**

Reviewers are leaf workers. At most two independent reviewers run when permitted; otherwise the axes run sequentially with shared context disclosed.

**What does a passing review establish?**

It reports the inspected scope and checks actually run. It does not establish deployment, signing, CI, or device acceptance.

## It's working if

- New and staged files appear in the reviewed scope.
- Findings name a concrete scenario, consequence, and location.
- The report states its base, head, scope, and validation limits.

## Where it fits

Read the [skill instructions](../../skills/engineering/code-review/SKILL.md) for its workflow. [ask-matt](ask-matt.md) maps the wider library.
