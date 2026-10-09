## What it does

Build behavior through red, green, and refactor cycles at public test boundaries. New tests must catch regressions using independently derived expected results.

## When to reach for it

Use for behavioral changes where meaningful regression tests are warranted. Existing task authorization and test conventions normally settle routine boundary choices.

## Common questions

**Must I approve every test boundary?**

No. Explicit approval gates remain in force, but ordinary tests at established boundaries proceed without another confirmation.

**Does every edit need a new test?**

No. Formatting, documentation, and reversible low-impact edits usually need existing checks. Match testing effort to the risk.

## It's working if

- The new test fails on the original behavior and passes after the fix.
- Tests observe outcomes rather than internal call structure.
- Refactoring keeps affected checks green.

## Where it fits

Read the [skill instructions](../../skills/engineering/tdd/SKILL.md) for its workflow. [ask-matt](ask-matt.md) maps the wider library.
