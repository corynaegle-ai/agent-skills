## What it does

Route a user to the relevant skill or workflow. Read the selected skill before recommending it, because the full entrypoint contains the actual behavior.

## When to reach for it

Select explicitly when unsure which skill fits. Only the recommended six are linked by default; optional flows need installation with their dependencies.

## Common questions

**Do I need the entire workflow for a small fix?**

No. Use the focused skill and existing project conventions. Basic debugging, design, and local review need no tracker setup.

**Which skill reviews whether tests provide value?**

Use [review-tests](review-tests.md) to audit and correct existing tests for real execution, independent assertions, refactor resilience, and reliability. Use [tdd](tdd.md) for new test-first implementation and [code-review](code-review.md) for a general change review.

**What changed in this fork?**

Routine choices reuse authorization, review captures uncommitted work, and parallel builds are bounded and verify the combined result.

## It's working if

- The recommendation fits the task size and uncertainty.
- Optional dependencies are identified.
- The user keeps control over planning and external publication.

## Where it fits

Read the [skill instructions](../../skills/engineering/ask-matt/SKILL.md) for its workflow. The [root index](../../README.md) lists all promoted skills.
