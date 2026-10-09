## What it does

Diagnose bugs around a feedback loop that catches the exact reported symptom. Reproduce and minimize where possible, test falsifiable hypotheses, fix, and rerun the original scenario.

## When to reach for it

Use for hard bugs, intermittent failures, and performance regressions. It can be explicitly selected or used when debugging fits.

## Common questions

**What if the failing environment is unavailable?**

Continue with available read-only evidence and clearly provisional hypotheses. Ask for missing access only when it prevents useful progress. Do not claim reproduction or verified repair without a suitable signal.

## It's working if

- The signal catches the user’s original symptom.
- Probes distinguish competing explanations.
- The final report separates confirmed evidence from unavailable validation.

## Where it fits

Read the [skill instructions](../../skills/engineering/diagnosing-bugs/SKILL.md) for its workflow. [ask-matt](ask-matt.md) maps the wider library.
