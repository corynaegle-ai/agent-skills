## What it does

Concentrate useful behavior behind small interfaces at testable seams. Evaluate leverage for callers and locality for maintainers while preserving the project’s established names.

## When to reach for it

Use for interface design, testability, or architectural friction. It is a reusable reference, not an instruction to refactor every touched module.

## Common questions

**Must existing services be renamed modules?**

No. Shared definitions clarify design without replacing the project’s established vocabulary.

**Should every dependency get an interface?**

Add seams where real variation or testing needs justify them; avoid hypothetical indirection.

## It's working if

- A caller learns less to accomplish its task.
- A change or bug fix concentrates in fewer places.
- Tests exercise meaningful behavior through the interface.

## Where it fits

Read the [skill instructions](../../skills/engineering/codebase-design/SKILL.md) for its workflow. [ask-matt](ask-matt.md) maps the wider library.
