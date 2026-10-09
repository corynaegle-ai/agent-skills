## What it does

Synthesize the existing conversation into a focused spec with acceptance criteria, implementation decisions, and test boundaries. Keep the requested scope rather than inventing an extensive feature backlog.

## When to reach for it

Select explicitly after requirements are settled. Use existing tracker configuration or default to `.scratch/<feature-slug>/spec.md` locally. Setup is optional for local work.

## Common questions

**Must I approve routine test boundaries again?**

No. Reuse established boundaries, state reasonable choices, and ask only about material behavior or architecture ambiguity.

**Does it interview me again?**

No. It works from the existing discussion and codebase evidence.

## It's working if

- The spec captures requested behavior and meaningful acceptance criteria.
- Test boundaries reuse the established design.
- Publication follows the authorized destination and scope.

## Where it fits

Read the [skill instructions](../../skills/engineering/to-spec/SKILL.md) for its workflow. [ask-matt](ask-matt.md) maps the wider library.
