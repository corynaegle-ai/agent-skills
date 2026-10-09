## What it does

Split authorized work into independently verifiable vertical slices with explicit blockers. Broad mechanical refactors use expand-contract sequencing where isolated vertical slices cannot stay green.

## When to reach for it

Select explicitly for work spanning several tasks or sessions. Use the configured tracker or default to local `.scratch/<feature-slug>/issues/` files when none is configured. Setup is optional for local work.

## Common questions

**Will it stop for another approval?**

It waits when the user requested a proposal or gated publication. An existing instruction to create tickets carries through when the breakdown stays within scope.

**What makes a useful ticket?**

A concrete observable outcome, acceptance criteria, and only the dependencies that actually gate its start.

## It's working if

- Each slice can be demonstrated or checked independently.
- Blocking edges correspond to real prerequisites.
- The published tickets match the requested work.

## Where it fits

Read the [skill instructions](../../skills/engineering/to-tickets/SKILL.md) for its workflow. [ask-matt](ask-matt.md) maps the wider library.
